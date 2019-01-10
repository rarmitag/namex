from hamcrest import *
from tests.support.seeds import seed_condition, seed_word, seed_word_condition, seed_condition_with_words


def test_conditions_list_displays_consenting_body(browser, base_url, db):
    seed_condition_with_words(db, consenting_body='this body needs to give approval', words='tdd, quality')

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
    seed_condition_with_words(db, consenting_body='this body needs to give approval', words='tdd, quality')

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
    seed_condition_with_words(db, consenting_body='this body needs to give approval', words='tdd, quality')

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


def test_consenting_body_update(browser, base_url, db):
    seed_condition_with_words(db, consenting_body='initial value', words='tdd, quality')

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    browser.find_element_by_link_text('initial value').click()

    cell_css = 'table.model-list tbody tr:nth-child(1) td.col-rc_consenting_body '
    browser.find_element_by_css_selector(cell_css + 'input').clear()
    browser.find_element_by_css_selector(cell_css + 'input').send_keys('new value')
    browser.find_element_by_css_selector(cell_css + 'button.editable-submit').click()

    browser.find_element_by_link_text('Virtual Word Condition').click()

    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('new value'))


def test_multiple_words_update(browser, base_url, db):
    seed_condition_with_words(db, consenting_body='initial value', words='tdd, quality')
    seed_condition_with_words(db, consenting_body='value2', words='new1, new2, new3, new4, new5')

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    browser.find_element_by_link_text('new1, new2, new3, new4, new5').click()

    cell_css = 'table.model-list tbody tr:nth-child(2) td.col-rc_words '
    browser.find_element_by_css_selector(cell_css + 'input').clear()
    browser.find_element_by_css_selector(cell_css + 'input').send_keys('new1, new2, new33, new44, new5')
    browser.find_element_by_css_selector(cell_css + 'button.editable-submit').click()

    browser.find_element_by_link_text('Virtual Word Condition').click()

    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('new1, new2, new33, new44, new5'))

def test_multiple_consenting_body_update(browser, base_url, db):
    seed_condition_with_words(db, consenting_body='initial value', words='tdd, quality')
    seed_condition_with_words(db, consenting_body='value2', words='new1, new2, new3, new4, new5')

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Virtual Word Condition').click()
    browser.find_element_by_link_text('value2').click()

    cell_css = 'table.model-list tbody tr:nth-child(2) td.col-rc_consenting_body '
    browser.find_element_by_css_selector(cell_css + 'input').clear()
    browser.find_element_by_css_selector(cell_css + 'input').send_keys('value3')
    browser.find_element_by_css_selector(cell_css + 'button.editable-submit').click()

    browser.find_element_by_link_text('Virtual Word Condition').click()

    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('value3'))
