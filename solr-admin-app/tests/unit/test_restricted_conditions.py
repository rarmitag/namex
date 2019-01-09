from hamcrest import *
from tests.support.seeds import seed_condition, seed_word, seed_word_condition


def test_conditions_list(browser, base_url, db):
    cnd_id = seed_condition(db, consenting_body='this body needs to give approval')
    tdd_id = seed_word(db, word='tdd')
    quality_id = seed_word(db, word='quality')
    seed_word_condition(db, cnd_id, tdd_id)
    seed_word_condition(db, cnd_id, quality_id)

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Word Condition').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Restricted Word Condition'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell_css = 'table.model-list tbody tr:nth-child(1) td:nth-child(2) '
    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('this body needs to give approval'))


def test_word_phrase_update(browser, base_url, db):
    seed_condition(db, cnd_id=1, consenting_body='this body needs to give approval')
    seed_word(db, cnd_id=1, word='tdd')
    seed_word(db, cnd_id=1, word='quality')

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Condition2').click()
    browser.find_element_by_link_text('tdd, quality').click()

    cell_css = 'table.model-list tbody tr:nth-child(1) td:nth-child(8) '
    browser.find_element_by_css_selector(cell_css + 'input').clear()
    browser.find_element_by_css_selector(cell_css + 'input').send_keys('TDD, quality')
    browser.find_element_by_css_selector(cell_css + 'button.editable-submit').click()

    browser.find_element_by_link_text('Restricted Condition2').click()

    cell = browser.find_element_by_css_selector(cell_css)
    assert_that(cell.text, equal_to('TDD, quality'))
