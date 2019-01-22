
import logging

import dotenv


# Load all the environment variables from a .env file located in the nearest directory above.

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

# Leave this as DEBUG for now.
logging.basicConfig(level=logging.DEBUG)



from tests.external.support.fake_oidc import FakeOidc


from solr_admin.keycloak import Keycloak
Keycloak._oidc = FakeOidc()

from solr_admin import create_application
application, admin = create_application(run_mode='testing')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
