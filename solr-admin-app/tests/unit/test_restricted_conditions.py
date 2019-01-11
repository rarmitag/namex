from hamcrest import *
from tests.support.seeds import *
from tests.unit.pages.word_condition_page import WordConditionPage


def test_conditions_list_displays_consenting_body(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='this body needs to give approval', words='tdd, quality')
    page = WordConditionPage(browser, base_url)

    assert_that(page.list_size(), equal_to(1))
    assert_that(page.consenting_body_of_row(1).text, equal_to('this body needs to give approval'))


def test_conditions_list_displays_restricted_words(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='this body needs to give approval', words='tdd, quality')
    page = WordConditionPage(browser, base_url)

    assert_that(page.list_size(), equal_to(1))
    assert_that(page.word_phrase_of_row(1).text, equal_to('tdd, quality'))


def test_word_phrase_update(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='this body needs to give approval', words='tdd, quality')
    page = WordConditionPage(browser, base_url)
    page.update(page.word_phrase_of_row(1), 'happy, new, year')
    page.refresh()

    assert_that(page.word_phrase_of_row(1).text, equal_to('happy, new, year'))


def test_consenting_body_update(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='initial value', words='tdd, quality')
    page = WordConditionPage(browser, base_url)
    page.update(page.consenting_body_of_row(1), 'new value')
    page.refresh()

    assert_that(page.consenting_body_of_row(1).text, equal_to('new value'))


def test_multiple_words_update(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='initial value', words='tdd, quality')
    seed_condition_and_words(db, consenting_body='value2', words='new1, new2, new3, new4, new5')
    page = WordConditionPage(browser, base_url)
    page.update(page.word_phrase_of_row(2), 'new1, new2, new33, new44, new5')
    page.refresh()

    assert_that(page.word_phrase_of_row(2).text, equal_to('new1, new2, new33, new44, new5'))


def test_multiple_consenting_body_update(browser, base_url, db):
    seed_condition_and_words(db, consenting_body='initial value', words='tdd, quality')
    seed_condition_and_words(db, consenting_body='value2', words='new1, new2, new3, new4, new5')
    page = WordConditionPage(browser, base_url)
    page.update(page.consenting_body_of_row(2), 'value3')
    page.refresh()

    assert_that(page.consenting_body_of_row(2).text, equal_to('value3'))
