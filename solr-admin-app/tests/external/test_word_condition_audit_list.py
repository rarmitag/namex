from hamcrest import *
from solr_admin.models.restricted_condition_audit import RestrictedConditionAudit


def test_word_conditon_audit_list(browser, base_url, db):
    db.session.add(RestrictedConditionAudit(username='rich', action='Create',cnd_id=1234, cnd_text='restricted word', words='help, me',
                    consent_required=True, consenting_body='me', instructions='Get consent', allow_use=True  ))
    db.session.commit()

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Condition Audit').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Restricted Condition Audit'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(2)')
    assert_that(cell.text, equal_to('rich'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(7)')
    assert_that(cell.text, equal_to('help, me'))
