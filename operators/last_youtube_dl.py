"""
Youtube-DL Operator
"""
from core.url_operator import OperatorInterface
from ydl.YoutubeDL import YoutubeDL

ydl = YoutubeDL()


class LastYoutubeDl(OperatorInterface):
    """YoutubeDl Operator"""

    priority = 0

    @classmethod
    def url_patterns(cls) -> list:
        return [
            r'https?'
        ]

    async def main(self, url: str):
        ie_result = ydl.extract_info(url, download=False)
        assert ie_result is not None

        streams = []
        for item in ie_result['formats']:
            item_to_append = {
                'src': [item['url']],
                'tbr': item['tbr'],
                'id': item['format_id'],
                'container': item['container'] if 'container' in item else '',
                'quality': item['format_note'],
            }
            if item['acodec'] != 'none':
                item_to_append['acodec'] = item['acodec']
            if item['vcodec'] != 'none':
                item_to_append['vcodec'] = item['vcodec']
            streams.append(item_to_append)
            streams = sorted(streams, key=lambda item: -float(item['tbr']))
        return {
            'streams': streams,
            'extractor': ie_result['extractor_key'],
            'extra': {}
        }
