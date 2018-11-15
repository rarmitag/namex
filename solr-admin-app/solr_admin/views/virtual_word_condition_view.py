
from flask import current_app, request, get_flashed_messages
from flask_admin.contrib import sqla

from solr_admin import keycloak
from solr_admin.services.create_records import create_records
from solr_admin.services.update_records import update_records


class VirtualWordConditionView(sqla.ModelView):

    column_labels = {
        'cnd_id': 'cnd_id',
        'word_id': 'word_id',
        'rc_consenting_body': 'consenting body',
        'rc_words': 'word phrase',
        'rc_condition_text': 'condition text',
        'rc_instructions': 'instructions',
        'rc_allow_use': 'allow use',
        'rc_consent_required': 'consent required'
    }

    action_disallowed_list = ['delete']

    can_export = True

    can_set_page_size = True

    column_editable_list = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    column_filters = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    column_searchable_list = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    create_template = 'generic_create.html'
    edit_template = 'generic_edit.html'
    list_template = 'generic_list.html'


    # At runtime determine whether or not the user has access to functionality of the view.
    def is_accessible(self):
        # Flask-OIDC function that states whether or not the user is logged in and has permissions.
        return keycloak.Keycloak(None).has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
        return keycloak.Keycloak(None).get_redirect_url(request.url)

    def after_model_change(self, form, model, is_created):
        if is_created:
            create_records(model, self.session)
        else:
            update_records(self.session)

    def after_model_delete(self, model):
        update_records(self.session)