"""
First Special Operator
"""
import asyncio
from core.url_operator import OperatorInterface
from core.util import nop


class FirstSpecial(OperatorInterface):
    """Operator should be the first to be executed"""

    priority = 100

    infoDict = {
        'https://www.bilibili.com/video/av92261?p=1': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P1. PART1)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-1.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=2': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P2. PART2)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-2.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=3': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P3. PART3)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-3.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=4': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P4. PART4)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-4.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=5': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P5. PART5)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-5.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=6': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P6. PART6)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-6.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=7': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P7. PART7)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-7.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=8': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P8. PART8)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-8.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=9': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P9. PART9)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-9.json', 'format': 'dash'},
        'https://www.bilibili.com/video/av92261?p=10': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P10. PART10)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/kkhta-10.json', 'format': 'dash'},
    }

    @classmethod
    def url_patterns(cls) -> list[str]:
        return list(cls.infoDict)

    async def main(self, url: str):
        await nop()
        info = self.infoDict[url]
        return {
            'streams': [{'src': [info['src']], 'container': info['format']}],
            'extractor': 'BiliBili', 'extra': {'danmaku': info['danmaku']}
        }
