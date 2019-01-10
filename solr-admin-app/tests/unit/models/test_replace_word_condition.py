from hamcrest import *

from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from tests.support.seeds import seed_word, seed_condition, seed_word_condition
from solr_admin.models.replace_word_condition import replace_word_condition


def test_update_association(db):
    cnd_id = seed_condition(db, consenting_body='any-condition')
    word_id = seed_word(db, word='any-word')
    seed_word_condition(db, cnd_id, word_id)
    replace_word_condition(db.session, cnd_id, 'any-new-word')

    result = db.session.query(RestrictedWordCondition).all()
    assert_that(len(result), equal_to(1))

    result = db.session.query(RestrictedWord).all()
    assert_that(len(result), equal_to(1))


def test_create_new_word(db):
    cnd_id = seed_condition(db, consenting_body='any-condition')
    word_id = seed_word(db, word='any-word')
    seed_word_condition(db, cnd_id, word_id)
    replace_word_condition(db.session, cnd_id, 'any-new-word')
    result = db.session.query(RestrictedWord).all()
    word = result[0].word_phrase

    assert_that(word, equal_to('any-new-word'))
