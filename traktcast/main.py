import logging
import os
import time

import pychromecast
import trakt

from traktcast.auth import TraktAuthHelper
from traktcast.controllers.hulu import HuluHandler
from traktcast.status_listener import MediaStatusListener

DEFAULT_TRAKT_CLIENT_ID = None


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('traktcast').setLevel(logging.DEBUG)

    trakt_client_id = os.environ.get('TRAKT_CLIENT_ID', None)
    if not trakt_client_id:
        logging.error('Missing trakt application ID, must be specified as TRAKT_CLIENT_ID environment variable')
    trakt.Trakt.configuration.defaults.client(id=trakt_client_id)

    trakt_auth_file = os.environ.get('TRAKT_AUTH', None)
    trakt_staging = os.environ.get('TRAKT_STAGING', False)
    if trakt_staging:
        trakt.Trakt.base_url = 'https://api-staging.trakt.tv'
        if not trakt_auth_file:
            trakt_auth_file = '~/.traktcast/auth.staging.json'

    auth = TraktAuthHelper(filename=trakt_auth_file)
    trakt.Trakt.configuration.defaults.oauth.from_response(auth.authenticate(), refresh=True)

    device = pychromecast.get_chromecast(friendly_name='Study')
    device.register_handler(HuluHandler(device))
    device.media_controller.register_status_listener(MediaStatusListener(device))

    while True:
        time.sleep(0.01)
