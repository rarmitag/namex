import time

from hamcrest import *


def authentification_is_needed(browser_against_real_keycloak, base_url):
    browser = browser_against_real_keycloak
    browser.get(base_url + '/admin/synonym')
    username = browser.find_element_by_css_selector('input#username')
    password = browser.find_element_by_css_selector('input#password')
    username.clear()
    password.clear()
    username.send_keys('names-with-admin-access')
    password.send_keys('WhatEver1')
    button = browser.find_element_by_css_selector('input#kc-login')
    button.click()
    time.sleep(1)

    assert_that(browser.current_url, equal_to(base_url + '/admin/synonym/'))


def has_access_from_keycloak(browser_against_real_keycloak, base_url):
    browser = browser_against_real_keycloak
    browser.get(base_url + '/admin/synonym')
    username = browser.find_element_by_css_selector('input#username')
    password = browser.find_element_by_css_selector('input#password')
    username.clear()
    password.clear()
    username.send_keys('names-no-admin-access')
    password.send_keys('WhatEver1')
    button = browser.find_element_by_css_selector('input#kc-login')
    button.click()
    time.sleep(1)

    body = browser.find_element_by_css_selector('body')
    assert_that(body.text, contains_string('not authorized'))