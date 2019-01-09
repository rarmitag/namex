
from flask import current_app, request
from flask_admin.contrib import sqla
from sqlalchemy import func

from solr_admin import keycloak

from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition


class VirtualWordConditionView(sqla.ModelView):

    column_list = ['cnd_id', 'word_id', 'rc_consenting_body', 'rc_words']
    column_labels = {
        'cnd_id': 'cnd_id',
        'word_id': 'word_id',
        'rc_consenting_body': 'consenting body',
        'rc_words': 'word phrase'
    }

    action_disallowed_list = ['delete']

    can_export = True

    can_set_page_size = True

    column_editable_list = ['rc_consenting_body', 'rc_words']

    column_filters = ['rc_consenting_body']

    column_searchable_list = ['rc_consenting_body']

    create_template = 'generic_create.html'
    edit_template = 'generic_edit.html'
    list_template = 'generic_list.html'

    def get_query(self):

        return self.session.query(RestrictedWordCondition, RestrictedCondition, RestrictedWord). \
            filter(RestrictedWordCondition.cnd_id == RestrictedCondition.cnd_id). \
            filter(RestrictedWordCondition.word_id == RestrictedWord.word_id). \
            order_by(RestrictedWordCondition.cnd_id, RestrictedWordCondition.word_id)

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(RestrictedWordCondition, RestrictedCondition). \
            filter(RestrictedWordCondition.cnd_id == RestrictedCondition.cnd_id)

    def _get_default_order(self):
        return None

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        count, query = sqla.ModelView.get_list(self, page, sort_column, sort_desc, search, filters, True, page_size)

        data = list()
        previous_word_condition = None
        for row in query:
            rwc, rc, rw = row
            word_condition = VirtualWordCondition(
                cnd_id=rwc.cnd_id,
                word_id=rwc.word_id,
                rc_consenting_body=rc.consenting_body,
                rc_words=rw.word_phrase
            )

            if previous_word_condition is None or word_condition.cnd_id != previous_word_condition.cnd_id:
                data.append(word_condition)
                previous_word_condition = word_condition
            else:
                previous_word_condition.rc_words += ', ' + rw.word_phrase

        return len(data), data

    # form_choices = {'cnd_text': RestrictedWord.cnd_text}
    # At runtime determine whether or not the user has access to functionality of the view. The rule is that data is
    # only editable in the test environment.
    def is_accessible(self):
        # Disallow editing unless in the 'testing' environment.
        editable = current_app.env == 'testing'
        self.can_create = editable
        self.can_delete = editable
        self.can_edit = editable

        if editable:
            # Make columns editable.
            self.column_editable_list = ['cnd_text','consent_required','consenting_body','instructions','allow_use','word_phrase']
        else:
            self.column_editable_list = []

        # Flask-OIDC function that states whether or not the user is logged in and has permissions.
        return keycloak.Keycloak(None).has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
        return keycloak.Keycloak(None).get_redirect_url(request.url)

    # When the user goes to save the data, trim whitespace and put the list back into alphabetical order.
    def on_model_change(self, form, model, is_created):
        pass
        # _validate_something??(model.cnd_text)

    # After saving the data create the audit log (we need to wait for a new id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            _create_audit_log(model, 'CREATE')
        else:
            _create_audit_log(model, 'UPDATE')

        from solr_admin.models.restricted_word import RestrictedWord
        try:
            RestrictedWord.query.filter_by(cnd_id=model.cnd_id).delete()
            word_phrase = form.data['word_phrase']
            for word in word_phrase.split(','):
                self.session.add(RestrictedWord(cnd_id=model.cnd_id, word=word))

            self.session.commit()
        except Exception:
            self.session.rollback()



    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        _create_audit_log(model, 'DELETE')

# Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
def _create_audit_log(model, action) -> None:
    pass
    #audit = restricted_condition_audit.RestrictedConditionAudit(
    #    keycloak.Keycloak(None).get_username(), action,  model.cnd_id, model.cnd_text, model.consent_required,
    #    model.consenting_body, model.instructions, model.allow_use)

    #session = models.db.session
    #session.add(audit)
    #session.commit()
