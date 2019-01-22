import os
import pytest
from selenium import webdriver

from solr_admin.models.virtual_word_condition import VirtualWordCondition
from tests.external.support.driver.server_driver import ServerDriver
from sqlalchemy.schema import MetaData, DropConstraint


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
    from solr_admin.models.restricted_condition import RestrictedCondition
    from solr_admin.models.restricted_word import RestrictedWord
    from solr_admin.models.restricted_word_condition import RestrictedWordCondition
    from tests.external.support.fake_oidc import FakeOidc
    from solr_admin.keycloak import Keycloak

    Keycloak._oidc = FakeOidc()
    app, admin = create_application(run_mode='testing')

    db = SQLAlchemy(app)
    metadata = MetaData(db.engine)
    metadata.reflect()
    for table in metadata.tables.values():
        for fk in table.foreign_keys:
            db.engine.execute(DropConstraint(fk.constraint))
    metadata.drop_all()
    db.drop_all()

    Synonym.metadata.create_all(bind=db.engine)
    RestrictedCondition.metadata.create_all(bind=db.engine)
    RestrictedWord.metadata.create_all(bind=db.engine)
    RestrictedWordCondition.metadata.create_all(bind=db.engine)
    VirtualWordCondition.metadata.create_all(bind=db.engine)

    return db


@pytest.fixture(scope="function")
def db(clean_db):
    yield clean_db
    clean_db.session.close()
