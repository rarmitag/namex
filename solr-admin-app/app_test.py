
import logging

import dotenv

import monkeypatch
import solr_admin

# Load all the environment variables from a .env file located in the nearest directory above.
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

# Leave this as DEBUG for now.
logging.basicConfig(level=logging.DEBUG)

# Do the unpleasant but necessary library monkeypatching.
monkeypatch.patch_ca_certs()


class FakeOidc:
    user_loggedin = True

    def user_getfield(self, key):
        return 'Joe'

    def user_role(self):
        return

    def has_access(self):
        return True

    def get_access_token(self):
        return 'any'

    def _get_token_info(self, token):
        return {'realm_access': {'roles': 'names_manager'}}


# Listen on all interfaces, and the catalog Python container expects the application to be on 8080.
application, admin = solr_admin.create_application(run_mode='testing')

from solr_admin.keycloak import Keycloak
Keycloak._oidc = FakeOidc()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
