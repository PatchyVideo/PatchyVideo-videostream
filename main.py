
# from flask import Flask, session, request, current_app
# app = Flask('VideoStream')

# from ydl.YoutubeDL import YoutubeDL
# ydl = YoutubeDL()
# from you_get.extractors import bilibili

# from json import dumps

# @app.route("/", methods = ['POST'])
# def entry() :
#     request_json = request.get_json()
#     try :
#         if 'bilibili.com' in request_json['url'] :
#             ret = bilibili.extract(request_json['url'], info_only = True)
#             ret = {'streams': ret, 'extractor': 'BiliBili'}
#             return current_app.response_class(dumps(ret) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])
#         ie_result = ydl.extract_info(request_json['url'], download = False)
#     except Exception as e :
#         return current_app.response_class(dumps({"vs_err": repr(e)}) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])
#     return current_app.response_class(dumps(ie_result) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])

# if __name__ == '__main__' or __name__ == 'main' :
#     app.run('0.0.0.0', 5006)

import asyncio

from aiohttp import web
from aiohttp import ClientSession

from you_get.extractors import bilibili
from ydl.YoutubeDL import YoutubeDL

ydl = YoutubeDL()

app = web.Application()
routes = web.RouteTableDef()

TMP_TABLE = {
	'https://www.bilibili.com/video/av92261?p=1': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P1. PART1)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P1. PART1).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=2': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P2. PART2)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P2. PART2).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=3': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P3. PART3)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P3. PART3).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=4': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P4. PART4)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P4. PART4).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=5': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P5. PART5)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P5. PART5).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=6': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P6. PART6)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P6. PART6).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=7': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P7. PART7)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P7. PART7).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=8': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P8. PART8)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P8. PART8).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=9': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P9. PART9)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P9. PART9).cmt.xml', 'format': 'dash'},
	'https://www.bilibili.com/video/av92261?p=10': {'src': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P10. PART10)_MP4.mpd', 'danmaku': 'https://thvideo.tv/kkhta/【東方手書】恋恋的♥心♥跳♥大冒险【PART1-10】 (P10. PART10).cmt.xml', 'format': 'dash'},
}

@routes.post("/")
async def entry(request) :
	try :
		url = (await request.json())['url']
		if url in TMP_TABLE :
			info = TMP_TABLE[url]
			ret = {'streams': [{'src': [info['src']], 'container': info['format']}], 'extractor': 'BiliBili', 'extra': {'danmaku': info['danmaku']}}
			return web.json_response(ret)
		if 'bilibili.com' in url :
			extractor_instance = bilibili.Bilibili()
			info = await extractor_instance.extract_info_only(url, info_only = True)
			for i in range(len(info)) :
				if '.mp4?' in info[i]['src'][0] :
					info[i]['container'] = 'mp4'
			extra_info = {}
			if hasattr(extractor_instance, 'video_cid') :
				extra_info['cid'] = extractor_instance.video_cid
			if hasattr(extractor_instance, 'lyrics') :
				extra_info['lyrics'] = extractor_instance.lyrics
			if hasattr(extractor_instance, 'danmaku') :
				extra_info['danmaku'] = extractor_instance.danmaku
			ret = {'streams': info, 'extractor': 'BiliBili', 'extra': extra_info}
			return web.json_response(ret)
		else :
			ie_result = ydl.extract_info(url, download = False)
			#return web.json_response(ie_result)
			streams = []
			for item in ie_result['formats'] :
				if item['acodec'] != 'none' and item['vcodec'] != 'none' :
					streams.append({
						'src': [item['url']],
						'id': item['format_id'],
						'container': item['container'] if 'container' in item else '',
						'quality': item['format_note']
					})
			ret = {'streams': streams, 'extractor': ie_result['extractor_key'], 'extra': {}}
			return web.json_response(ret)
	except Exception as e :
		return web.json_response({"vs_err": repr(e)})

app.add_routes(routes)

async def start_async_app():
	# schedule web server to run
	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, '0.0.0.0', 5006)
	await site.start()
	print("Serving up app on 0.0.0.0:5006")
	return runner, site

loop = asyncio.get_event_loop()
runner, site = loop.run_until_complete(start_async_app())

try:
	loop.run_forever()
except KeyboardInterrupt as err:
	loop.run_until_complete(runner.cleanup())


