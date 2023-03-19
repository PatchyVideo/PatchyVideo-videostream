"""Twitter Operator"""
import json
import re
from core.url_operator import OperatorInterface
from you_get.common import match1, r1
from aiohttp import ClientSession


class Twitter(OperatorInterface):
    """Twitter Operator"""

    authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

    ga_url = 'https://api.twitter.com/1.1/guest/activate.json'

    api_url = 'https://api.twitter.com/1.1/statuses/show.json?id=%s&tweet_mode=extended&include_entities=true'

    @classmethod
    def url_patterns(cls) -> list:
        return [
            r"https?://(mobile\.)?twitter\.com/[a-zA-Z0-9_-]+"
        ]

    async def main(self, url: str):
        link = ('https://' + str(match1(url, r"//mobile\.(.+)"))
                ) if re.match(r'https?://mobile', url) else url
        item_id = r1(r'twitter\.com/[^/]+/status/(\d+)', link)

        async with ClientSession() as session:
            async with session.post(
                    Twitter.ga_url,
                    headers={'authorization': Twitter.authorization}
            ) as resp:
                ga_content = await resp.text()

            guest_token = json.loads(ga_content)['guest_token']

            async with session.get(
                Twitter.api_url % item_id,
                headers={'authorization': Twitter.authorization,
                         'x-guest-token': guest_token}
            ) as resp:
                api_content = await resp.text()

            info = json.loads(api_content)
            mtype = 'none'
            murls = []

            if 'entities' in info and 'media' in info['entities']:
                for item in info['entities']['media']:
                    if 'media_url' in item:
                        media_url = item['media_url']
                        murls.append(media_url)
                        if ('ext_tw_video_thumb' in media_url
                                and mtype == 'none'):
                            mtype = 'video'
                        elif mtype == 'none':
                            mtype = 'image'

            if (mtype == 'video'
                and 'extended_entities' in info
                    and 'video_info' in info['extended_entities']['media'][0]):
                variants = info['extended_entities']['media'][0]['video_info']['variants']
                return {
                    'streams': [
                        {
                            'src': [item['url'].replace(
                                'https://video.twimg.com/ext_tw_video',
                                'https://thvideo.tv/twitter-video'
                            )],
                            'container': 'mp4',
                            'bitrate': item['bitrate']
                        } for item in variants
                        if item['content_type'] == 'video/mp4'
                    ]
                }
            return {'stream': []}
