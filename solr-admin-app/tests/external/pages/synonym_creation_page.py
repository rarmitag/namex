import time


class SynonymCreationPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.refresh()

    def refresh(self):
        self.browser.find_element_by_link_text('Synonym').click()
        self.browser.find_element_by_link_text('Create').click()

    def fill(self, id, value):
        cell = self.browser.find_element_by_css_selector('input#'+id)
        cell.send_keys(value)

    def save(self):
        form = self.browser.find_element_by_css_selector('form')
        form.submit()
        time.sleep(1)
