import pytest
from hamcrest import *

from tests.conftest import get_browser, connect_with


@pytest.fixture(scope="session")
def new_server(server):
    yield server
    server.shutdown()


@pytest.fixture(scope="session")
def new_browser(new_server, base_url):
    browser = get_browser()
    browser.get(base_url + '/admin/synonym')
    connect_with(browser, login='names-no-admin-access')
    yield browser
    browser.quit()


def test_cannot_access_synonyms(new_browser, base_url):
    browser = new_browser
    browser.get(base_url + '/admin/synonym')
    body = browser.find_element_by_tag_name('body')

    assert_that(body.text, contains_string('not authorized'))


def test_cannot_access_virtual_word_condition(new_browser, base_url):
    browser = new_browser
    browser.get(base_url + '/admin/virtualwordcondition')
    body = browser.find_element_by_tag_name('body')

    assert_that(body.text, contains_string('not authorized'))



