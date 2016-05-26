import json
import logging
import os
import threading

import trakt

log = logging.getLogger(__name__)


class TraktAuthHelper(object):
    def __init__(self, filename=None):
        self.filename = os.path.expanduser(filename or '~/.traktcast/auth.json')

        self.is_authenticating = threading.Condition()
        self.authorization = None

        # Bind trakt events
        trakt.Trakt.on('oauth.token_refreshed', self.on_token_refreshed)

    def authenticate(self):
        if not self.is_authenticating.acquire(blocking=False):
            logging.warning('Authentication has already been started')
            return False

        if self.filename and os.path.exists(self.filename):
            with open(self.filename, 'r') as fp:
                try:
                    self.authorization = json.load(fp)
                except json.JSONDecodeError as e:
                    log.error('Could not read authorization from %s', self.filename, exc_info=e)
                else:
                    if self.authorization:
                        log.debug('Loaded authorization from %s', self.filename)
                        return self.authorization

        # Request new device code
        code = trakt.Trakt['oauth/device'].code()

        print('Enter the code "%s" at %s to authenticate your account' % (
            code.get('user_code'),
            code.get('verification_url')
        ))

        # Construct device authentication poller
        poller = (trakt.Trakt['oauth/device'].poll(**code)
                  .on('aborted', self.on_aborted)
                  .on('authenticated', self.on_authenticated)
                  .on('expired', self.on_expired)
                  .on('poll', self.on_poll))

        # Start polling for authentication token
        poller.start(daemon=False)

        # Wait for authentication to complete
        if self.is_authenticating.wait():
            return self.authorization
        else:
            return None

    def on_aborted(self):
        """Triggered when device authentication was aborted (either with `DeviceOAuthPoller.stop()`
           or via the "poll" event)"""

        logging.error('Authentication aborted')

        # Authentication aborted
        self.is_authenticating.acquire()
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_authenticated(self, authorization):
        """Triggered when device authentication has been completed
        :param authorization: Authentication token details
        :type authorization: dict
        """

        # Acquire condition
        self.is_authenticating.acquire()

        # Store authorization for future calls
        self.authorization = authorization

        if self.filename:
            try:
                path = os.path.dirname(self.filename)
                if not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)

                with open(self.filename, 'w') as fp:
                    json.dump(self.authorization, fp, sort_keys=True, indent=4, separators=(',', ': '))
            except Exception as e:
                log.error('Could not save authorization to %s', self.filename, exc_info=e)

        logging.debug('Authentication successful - authorization: %r', self.authorization)

        # Authentication complete
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_expired(self):
        """Triggered when the device authentication code has expired"""

        logging.warning('Authentication expired')

        # Authentication expired
        self.is_authenticating.acquire()
        self.is_authenticating.notify_all()
        self.is_authenticating.release()

    def on_poll(self, callback):
        """Triggered before each poll
        :param callback: Call with `True` to continue polling, or `False` to abort polling
        :type callback: func
        """

        # Continue polling
        callback(True)

    def on_token_refreshed(self, authorization):
        # OAuth token refreshed, store authorization for future calls
        self.authorization = authorization

        logging.debug('Token refreshed - authorization: %r', self.authorization)
