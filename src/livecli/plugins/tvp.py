import re

from livecli.exceptions import PluginError
from livecli.plugin import Plugin
from livecli.plugin.api import http
from livecli.plugin.api import useragents
from livecli.stream import HLSStream
from livecli.stream import HTTPStream


class TVP(Plugin):
    '''Telewizja Polska S.A.
       http://tvpstream.vod.tvp.pl
    '''

    player_url = 'https://www.tvp.pl/sess/tvplayer.php?object_id={0}&autoplay=true'

    _url_re = re.compile(r'https?://tvpstream\.vod\.tvp\.pl')
    _stream_re = re.compile(r'''src:["'](?P<url>[^"']+\.(?:m3u8|mp4))["']''')
    _video_id_re = re.compile(r'''class=["']tvp_player["'][^>]+data-video-id=["'](?P<video_id>\d+)["']''')

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url) is not None

    def get_embed_url(self):
        res = http.get(self.url)

        m = self._video_id_re.search(res.text)
        if not m:
            raise PluginError('Unable to find a video id')

        video_id = m.group('video_id')
        self.logger.debug('Found video id: {0}'.format(video_id))
        p_url = self.player_url.format(video_id)
        return p_url

    def _get_streams(self):
        http.headers.update({'User-Agent': useragents.FIREFOX})

        embed_url = self.get_embed_url()
        res = http.get(embed_url)
        m = self._stream_re.findall(res.text)
        if not m:
            raise PluginError('Unable to find a stream url')

        streams = []
        for url in m:
            self.logger.debug('URL={0}'.format(url))
            if url.endswith('.m3u8'):
                for s in HLSStream.parse_variant_playlist(self.session, url, name_fmt='{pixels}_{bitrate}').items():
                    streams.append(s)
            elif url.endswith('.mp4'):
                streams.append(('vod', HTTPStream(self.session, url)))

        return streams


__plugin__ = TVP
