import time

from selenium.webdriver.common.by import By


class WordConditionListPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.browser.get(base_url + '/')
        self.browser.find_element_by_tag_name('a').click()
        self.refresh()

    def refresh(self):
        self.browser.find_element_by_link_text('Virtual Word Condition').click()

    def list_size(self):
        rows_css = 'table.model-list tbody tr '
        rows = self.browser.find_elements_by_css_selector(rows_css)

        return len(rows) if 'There are no items in the table' not in rows[0].text else 0

    def search(self, criteria):
        search_field = self.browser.find_element(By.NAME, "search")
        search_field.clear()
        search_field.send_keys(criteria)
        search_field.submit()
        time.sleep(1)

    def row(self, index):
        return 'table.model-list tbody tr:nth-child(' + str(index) + ') '

    def element(self, what, index):
        selector = self.row(index) + what
        cell = self.browser.find_element_by_css_selector(selector)

        return cell

    def consenting_body_of_row(self, index):
        return self.element('td.col-rc_consenting_body ', index)

    def word_phrase_of_row(self, index):
        return self.element('td.col-rc_words ', index)

    def condition_text_of_row(self, index):
        return self.element('td.col-rc_condition_text ', index)

    def instructions_of_row(self, index):
        return self.element('td.col-rc_instructions ', index)

    def update_with_value(self, cell, value):
        cell.find_element_by_css_selector('a').click()
        cell.find_element_by_css_selector('input').clear()
        cell.find_element_by_css_selector('input').send_keys(value)
        cell.find_element_by_css_selector('button.editable-submit').click()

    def update(self, cell, value):
        self.update_with_value(cell, value)

    def delete_record(self, index):
        button = self.element('td.list-buttons-column button', index)
        button.click()
        alert = self.browser.switch_to.alert
        alert.accept()
        time.sleep(1)


