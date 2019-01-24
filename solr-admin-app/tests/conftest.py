import os
import pytest
from selenium import webdriver
from sqlalchemy import engine_from_config
from tests.external.support.driver.server_driver import ServerDriver


@pytest.fixture(scope="session")
def port():
    return 8080


@pytest.fixture(scope="function")
def server_with_real_keycloak(port):
    app = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    server = ServerDriver(name='MyServer', port=port)
    server.start(cmd=['python', app])
    return server


@pytest.fixture(scope="function")
def server_with_fake_keycloak(port):
    app = os.path.join(os.path.dirname(__file__), '..', 'tests', 'external', 'support', 'app_test.py')
    server = ServerDriver(name='MyServer', port=port)
    server.start(cmd=['python', app])
    return server


def get_browser():
    import os
    import platform
    gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'mac', 'geckodriver')
    if platform.system() == 'Linux':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'linux', 'geckodriver')
    if platform.system() == 'Windows':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'windows', 'geckodriver.exe')

    return webdriver.Firefox(executable_path=gecko)


@pytest.fixture(scope="function")
def browser_against_real_keycloak(server_with_real_keycloak):
    browser = get_browser()
    yield browser
    browser.quit()
    server_with_real_keycloak.shutdown()


@pytest.fixture(scope="function")
def browser(server_with_fake_keycloak):
    browser = get_browser()
    yield browser
    browser.quit()
    server_with_fake_keycloak.shutdown()


@pytest.fixture(scope="session")
def base_url(port):
    return 'http://localhost:' + str(port)


@pytest.fixture(scope="function")
def clean_db():
    from flask_sqlalchemy import SQLAlchemy
    from solr_admin import create_application
    from solr_admin.models.synonym import Synonym
    from solr_admin.models.synonym_audit import SynonymAudit
    from solr_admin.models.restricted_condition import RestrictedCondition
    from solr_admin.models.restricted_word import RestrictedWord
    from solr_admin.models.restricted_word_condition import RestrictedWordCondition
    from solr_admin.models.virtual_word_condition import VirtualWordCondition
    from tests.external.support.fake_oidc import FakeOidc
    from solr_admin.keycloak import Keycloak

    Keycloak._oidc = FakeOidc()
    app, admin = create_application(run_mode='testing')

    db = SQLAlchemy(app)

    synonyms_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_BINDS']['synonyms']})
    Synonym.metadata.drop_all(bind=synonyms_db)
    Synonym.metadata.create_all(bind=synonyms_db, tables=[Synonym.metadata.tables['synonym']])
    SynonymAudit.metadata.create_all(bind=synonyms_db, tables=[SynonymAudit.metadata.tables['synonym_audit']])

    namex_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_DATABASE_URI']})
    RestrictedCondition.metadata.drop_all(bind=namex_db)
    RestrictedCondition.metadata.create_all(bind=namex_db, tables=[RestrictedCondition.metadata.tables['restricted_condition']])
    RestrictedWord.metadata.create_all(bind=namex_db, tables=[RestrictedWord.metadata.tables['restricted_word']])
    RestrictedWordCondition.metadata.create_all(bind=namex_db, tables=[RestrictedWordCondition.metadata.tables['restricted_word_condition']])
    VirtualWordCondition.metadata.create_all(bind=namex_db, tables=[VirtualWordCondition.metadata.tables['virtual_word_condition']])

    return db


@pytest.fixture(scope="function")
def db(clean_db):
    yield clean_db
    clean_db.session.close()
