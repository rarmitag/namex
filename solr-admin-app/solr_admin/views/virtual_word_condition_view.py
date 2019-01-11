
from flask import current_app, request, get_flashed_messages
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib import sqla
from sqlalchemy import func
from werkzeug.exceptions import abort

from solr_admin import keycloak

from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.models.replace_word_condition import replace_word_condition

class VirtualWordConditionView(sqla.ModelView):

    column_list = ['cnd_id', 'word_id', 'rc_consenting_body', 'rc_words', 'rc_condition_text']
    column_labels = {
        'cnd_id': 'cnd_id',
        'word_id': 'word_id',
        'rc_consenting_body': 'consenting body',
        'rc_words': 'word phrase',
        'rc_condition_text': 'condition text'
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

        query = self.get_query()
        query = self._apply_pagination(query, page, page_size)
        query = query.all()

        data = list()
        previous_word_condition = None
        for row in query:
            rwc, rc, rw = row
            word_condition = VirtualWordCondition(
                cnd_id=rwc.cnd_id,
                word_id=rwc.word_id,
                rc_consenting_body=rc.consenting_body,
                rc_words=rw.word_phrase,
                rc_condition_text=rc.cnd_text
            )
            keep = True
            if search:
                keep = search in rc.consenting_body

            if keep:
                if previous_word_condition is None or word_condition.cnd_id != previous_word_condition.cnd_id:
                    data.append(word_condition)
                    previous_word_condition = word_condition
                else:
                    previous_word_condition.rc_words += ', ' + rw.word_phrase

        return len(data), data

    # At runtime determine whether or not the user has access to functionality of the view.
    def is_accessible(self):
        # Flask-OIDC function that states whether or not the user is logged in and has permissions.
        return keycloak.Keycloak(None).has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
        return keycloak.Keycloak(None).get_redirect_url(request.url)

    @expose('/ajax/update/', methods=('POST',))
    def ajax_update(self):
        if not self.column_editable_list:
            abort(404)

        form = self.list_form()
        fields = list(form)

        def value(name):
            for field in fields:
                if field.name == name:
                    return field.data

        consenting_body = value('rc_consenting_body')
        rc_words = value('rc_words')
        cnd_id = value('list_form_pk').split(',')[0]

        if rc_words is not None:
            replace_word_condition(self.session, cnd_id, rc_words)

        if consenting_body is not None:
            try:
                condition = self.session.query(RestrictedCondition).filter_by(cnd_id=cnd_id).first()
                condition.consenting_body = consenting_body
                self.session.commit()
            except Exception:
                self.session.rollback()

        return gettext('Record was successfully saved.')


