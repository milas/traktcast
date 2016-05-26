import logging

import pychromecast.controllers
import pychromecast.controllers.media

from traktcast.controllers.hulu.api import HuluApi

log = logging.getLogger(__name__)


class HuluHandler(object):
    def __init__(self, device: pychromecast.Chromecast):
        self.device = device

        self.namespace = "urn:x-cast:com.hulu.plus"
        self._client = HuluApi()
        self._video_id = -1
        self._content_id = -1

    def registered(self, socket_client):
        pass

    def channel_connected(self):
        pass

    def channel_disconnected(self):
        pass

    # pylint: disable=unused-argument
    def receive_message(self, message, data: dict) -> bool:
        event_type = data.get('event_type', None)
        event_data = data.get('data', {})
        if not event_type:
            log.warning('Message missing event type (message_id=%d)', data.get('message_id', -1))
            return

        if event_type == 'current_settings':
            hulu_data = event_data.get('autoplay', {})
            if not self._client.token and 'access_token' in hulu_data:
                self._client.token = hulu_data['access_token']
            return True
        elif event_type == 'playback_update':
            content_id = event_data.get('content_id', -1)
            if content_id != -1 and self._content_id != content_id:
                video = self._client.get_video_by_content_id(content_id)
                if video:
                    self._content_id = content_id
                    self.device.media_controller.status.update(
                        {
                            'status': [{
                                'media': {'metadata': video}
                            }],
                        }
                    )
            return True
        else:
            log.debug('Unsupported Hulu event %s', event_type)
