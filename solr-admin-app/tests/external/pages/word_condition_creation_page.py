import time


class WordConditionCreationPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.browser.get(base_url + '/')
        self.browser.find_element_by_tag_name('a').click()
        self.refresh()

    def refresh(self):
        self.browser.find_element_by_link_text('Restricted Word Condition').click()
        self.browser.find_element_by_link_text('Create').click()

    def fill(self, id, value):
        cell = self.browser.find_element_by_css_selector('input#'+id)
        cell.send_keys(value)

    def save(self):
        form = self.browser.find_element_by_css_selector('form')
        form.submit()
        time.sleep(1)