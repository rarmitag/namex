from hamcrest import *
from tests.support.seeds import seed_condition, seed_word, seed_word_condition


def test_conditions_list_displays_consenting_body(browser, base_url, db):
    cnd_id = seed_condition(db, consenting_body='this body needs to give approval')
    tdd_id = seed_word(db, word='tdd')
    quality_id = seed_word(db, word='quality')
    seed_word_condition(db, cnd_id, tdd_id)
    seed_word_condition(db, cnd_id, quality_id)

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Virtual Word Condition'))
    assert_that(selection[1].text, equal_to('List (1)'))

    consenting_body_selector = 'table.model-list tbody tr:nth-child(1) td.col-rc_consenting_body '
    cell = browser.find_element_by_css_selector(consenting_body_selector)
    assert_that(cell.text, equal_to('this body needs to give approval'))


def test_conditions_list_displays_restricted_words(browser, base_url, db):
    cnd_id = seed_condition(db, consenting_body='this body needs to give approval')
    tdd_id = seed_word(db, word='tdd')
    quality_id = seed_word(db, word='quality')
    seed_word_condition(db, cnd_id, tdd_id)
    seed_word_condition(db, cnd_id, quality_id)

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Virtual Word Condition'))
    assert_that(selection[1].text, equal_to('List (1)'))

    words_selector = 'table.model-list tbody tr:nth-child(1) td.col-rc_words '
    cell = browser.find_element_by_css_selector(words_selector)
    assert_that(cell.text, equal_to('tdd, quality'))


def test_word_phrase_update(browser, base_url, db):
    cnd_id = seed_condition(db, consenting_body='this body needs to give approval')
    tdd_id = seed_word(db, word='tdd')
    quality_id = seed_word(db, word='quality')
    seed_word_condition(db, cnd_id, tdd_id)
    seed_word_condition(db, cnd_id, quality_id)

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    browser.find_element_by_link_text('tdd, quality').click()

    cell_css = 'table.model-list tbody tr:nth-child(1) td.col-rc_words '
    browser.find_element_by_css_selector(cell_css + 'input').clear()
    browser.find_element_by_css_selector(cell_css + 'input').send_keys('happy, new, year')
    browser.find_element_by_css_selector(cell_css + 'button.editable-submit').click()

    browser.find_element_by_link_text('Virtual Word Condition').click()

    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('happy, new, year'))
