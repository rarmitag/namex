from hamcrest import *
from solr_admin import create_application
from solr_admin.views.virtual_word_condition_view import VirtualWordConditionView


def test_word_condition_view_name():
    application, admin = create_application('testing')
    view = None
    for candidate in admin._views:
        if type(candidate) is VirtualWordConditionView:
            view = candidate
            break

    assert_that(view, not_none())
    assert_that(view.name, equal_to('Virtual Word Condition'))
