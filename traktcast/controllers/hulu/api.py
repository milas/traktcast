import functools
import logging
import re

import pychromecast.controllers.media
import requests

log = logging.getLogger(__name__)


class HuluApi(object):
    base_url = 'http://mozart.hulu.com/v1.h2o'

    def __init__(self):
        self.token = None

    @functools.lru_cache(maxsize=10)
    def get_video_by_content_id(self, content_id):
        resp = requests.head('http://www.hulu.com/watch', params={'content_id': content_id}, allow_redirects=True)
        video_id = re.search('/watch/(?P<video_id>[\d]+)', resp.url)
        if video_id:
            return self.get_video(int(video_id.group('video_id')))

    @functools.lru_cache(maxsize=10)
    def get_video(self, video_id: int) -> dict:
        if not self.token:
            self._authorize()

        def do_request():
            return requests.get(self.base_url + '/videos/' + str(video_id), params={'access_token': self.token})

        resp = do_request()
        if resp.status_code == 403:
            if not self._authorize():
                log.error('Could not authorize!')
                return None
            resp = do_request()

        if resp.status_code != 200:
            return None

        data = resp.json()['data'][0]['video']
        metadata = {
            'id': data.get('id', -1),
            'content_id': data.get('content_id', -1),
            'title': data.get('title', None),
            'seriesTitle': data.get('show', {}).get('name', None),
            'season': data.get('season_number', None),
            'episode': data.get('episode_number', None)
        }

        video_type = data.get('programming_type', None) or ''
        if video_type.upper() == 'FULL EPISODE':
            metadata['metadataType'] = pychromecast.controllers.media.METADATA_TYPE_TVSHOW

        return metadata

    def _authorize(self) -> bool:
        resp = requests.get('http://www.hulu.com/tv')
        token = re.search("w.API_DONUT = '(?P<token>[^']*)'", resp.text)
        if token:
            self.token = token.group('token')
            return True

        return False
