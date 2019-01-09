from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.views.virtual_word_condition_view import VirtualWordConditionView
from solr_admin.models.restricted_condition import RestrictedCondition
from tests.support.seeds import seed_condition, seed_word, seed_full_condition, seed_word_condition
from hamcrest import *


def test_aggregation(db):
    cnd_id = seed_condition(db, consenting_body='needs approval')
    tdd_id = seed_word(db, word='tdd')
    quality_id = seed_word(db, word='quality')
    seed_word_condition(db, cnd_id, tdd_id)
    seed_word_condition(db, cnd_id, quality_id)
    view = VirtualWordConditionView(VirtualWordCondition, db.session)
    count, data = view.get_list(page=0, sort_column=None, sort_desc=None, search=None, filters=None)

    assert_that(count, equal_to(1))
    assert_that(data[0].cnd_id, equal_to(cnd_id))
    assert_that(data[0].rc_consenting_body, equal_to('needs approval'))
    assert_that(data[0].rc_words, equal_to('tdd, quality'))


def test_respect_creation_order(db):
    cnd_1 = seed_condition(db, consenting_body='condition-1')
    cnd_2 = seed_condition(db, consenting_body='condition-2')
    quality_id = seed_word(db, word='quality')
    word_2 = seed_word(db, word='word-2')
    tdd_id = seed_word(db, word='tdd')
    seed_word_condition(db, cnd_1, quality_id)
    seed_word_condition(db, cnd_2, word_2)
    seed_word_condition(db, cnd_1, tdd_id)
    view = VirtualWordConditionView(VirtualWordCondition, db.session)
    count, data = view.get_list(page=0, sort_column=None, sort_desc=None, search=None, filters=None)

    assert_that(count, equal_to(2))
    assert_that(data[0].cnd_id, equal_to(cnd_1))
    assert_that(data[0].rc_consenting_body, equal_to('condition-1'))
    assert_that(data[0].rc_words, equal_to('quality, tdd'))
    assert_that(data[1].cnd_id, equal_to(cnd_2))
    assert_that(data[1].rc_consenting_body, equal_to('condition-2'))
    assert_that(data[1].rc_words, equal_to('word-2'))


