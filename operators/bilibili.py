"""
Bilibili Operator
"""
from core.url_operator import OperatorInterface
from you_get.extractors import bilibili


class Bilibili(OperatorInterface):
    """Bilibili Operator"""

    @classmethod
    def url_patterns(cls) -> list:
        return [
            r"https?://(www\.)?bilibili\.com/video/[a-zA-Z0-9_-]+"
        ]

    async def main(self, url: str):
        instance = bilibili.Bilibili(url)
        instance.prepare()
        instance.extract()
        info = instance.streams_sorted
        if not info and instance.dash_streams:
            info = [
                {
                    "container": 'dash',
                    "id": k,
                    "quality": v['quality'],
                    "src":[src[0] for src in v['src']],
                    "size":v['size']
                }
                for _, (k, v) in enumerate(instance.dash_streams.items())
            ]

        if info:
            for _, v in enumerate(info):
                if '.mp4?' in v['src'][0]:
                    v['container'] = 'mp4'

        extra_info = {}

        if hasattr(instance, 'vid'):
            extra_info['cid'] = instance.vid
        if hasattr(instance, 'lyrics'):
            extra_info['lyrics'] = instance.lyrics
        if hasattr(instance, 'danmaku'):
            extra_info['danmaku'] = instance.danmaku
        # FIXME: no attr
        # if hasattr(instance, 'duration_ms'):
        #     extra_info['duration_ms'] = instance.duration_ms
        # else:
        extra_info['duration_ms'] = 0

        return {'streams': info, 'extractor': 'BiliBili', 'extra': extra_info}
