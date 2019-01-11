from hamcrest import *
from tests.support.seeds import *
from tests.unit.pages.word_condition_page import WordConditionPage


def test_considers_consenting_body(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='needs approval', words='bc, british')
    seed_condition_and_words(db, consenting_body='needs signature', words='royal, queen')
    page = WordConditionPage(browser, base_url)

    assert_that(page.list_size(), equal_to(2))
    page.search('approval')

    assert_that(page.list_size(), equal_to(1))
    assert_that(page.consenting_body_of_row(1).text, equal_to('needs approval'))


def test_applies_or_between_searched_words(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='one two three', words='any')
    seed_condition_and_words(db, consenting_body='one two four', words='any')
    seed_condition_and_words(db, consenting_body='five six', words='any')
    page = WordConditionPage(browser, base_url)

    assert_that(page.list_size(), equal_to(3))
    page.search('one three')

    assert_that(page.list_size(), equal_to(2))
    assert_that(page.consenting_body_of_row(1).text, equal_to('one two three'))
    assert_that(page.consenting_body_of_row(2).text, equal_to('one two four'))


def test_considers_word_phrase(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='needs approval', words='bc, british')
    seed_condition_and_words(db, consenting_body='needs signature', words='royal, queen')
    seed_condition_and_words(db, consenting_body='needs magic', words='royal, queen, crown')
    page = WordConditionPage(browser, base_url)
    page.search('queen')

    assert_that(page.list_size(), equal_to(2))
    assert_that(page.consenting_body_of_row(1).text, equal_to('needs signature'))
    assert_that(page.consenting_body_of_row(2).text, equal_to('needs magic'))