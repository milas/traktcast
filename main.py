import logging
import time

import pychromecast

from traktcast.trakt import configure_trakt_client
from traktcast.hulu import HuluHandler
from traktcast.scrobble import TraktScrobblerListener


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('traktcast').setLevel(logging.DEBUG)

    configure_trakt_client()

    devices = pychromecast.get_chromecasts()
    for device in devices:
        device.register_handler(HuluHandler(device))
        device.media_controller.register_status_listener(TraktScrobblerListener(device))

    while True:
        time.sleep(0.01)
