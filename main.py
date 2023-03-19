
import asyncio
import json
import re

from aiohttp import web
from aiohttp import ClientSession

from you_get.extractors import bilibili
from ydl.YoutubeDL import YoutubeDL
from you_get.common import match1, r1

ydl = YoutubeDL()

app = web.Application()
routes = web.RouteTableDef()

authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

TMP_TABLE = {
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
			if not info and extractor_instance.dash_streams :
				streams = extractor_instance.dash_streams
				info = []
				for i, (k, v) in enumerate(streams.items()) :
					info.append({
						'container': 'dash',
						'id': k,
						'quality': v['quality'],
						'src': [src[0] for src in v['src']],
						'size': v['size']
					})
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
			if extractor_instance.duration_ms :
				extra_info['duration_ms'] = extractor_instance.duration_ms
			else :
				extra_info['duration_ms'] = 0
			ret = {'streams': info, 'extractor': 'BiliBili', 'extra': extra_info}
			return web.json_response(ret)
		elif 'twitter.com' in url :
			if re.match(r'https?://mobile', url): # normalize mobile URL
				link = 'https://' + match1(url, r'//mobile\.(.+)')
			screen_name = r1(r'twitter\.com/([^/]+)', url)
			item_id = r1(r'twitter\.com/[^/]+/status/(\d+)', url)
			async with ClientSession() as session:
				ga_url = 'https://api.twitter.com/1.1/guest/activate.json'
				async with session.post(ga_url, headers = {'authorization': authorization}) as resp:
					ga_content = await resp.text()
				guest_token = json.loads(ga_content)['guest_token']
				api_url = 'https://api.twitter.com/1.1/statuses/show.json?id=%s&tweet_mode=extended&include_entities=true' % item_id
				async with session.get(api_url, headers = {'authorization': authorization, 'x-guest-token': guest_token}) as resp:
					api_content = await resp.text()
				info = json.loads(api_content)
				id_str = info['id_str']
				mtype = 'none'
				murls = []
				if 'entities' in info and 'media' in info['entities'] :
					for item in info['entities']['media'] :
						if 'media_url' in item :
							media_url = item['media_url']
							murls.append(media_url)
							if 'ext_tw_video_thumb' in media_url and mtype == 'none' :
								mtype = 'video'
							elif mtype == 'none' :
								mtype = 'image'
				if mtype == 'video' and 'extended_entities' in info and 'video_info' in info['extended_entities']['media'][0] :
					# try :
					# 	db.media_meta.insert_one({
					# 		'id': id_str,
					# 		'sn': info['user']['screen_name'],
					# 		'text': info['text'],
					# 		'type': 'video',
					# 		'urls': [item['url'] for item in info['extended_entities']['media'][0]['video_info']['variants']],
					# 		'downloaded': False
					# 	})
					# 	vid_cnt += 1
					# except :
					# 	pass
					return web.json_response({'streams':[{'src':[item['url'].replace('https://video.twimg.com/ext_tw_video', 'https://thvideo.tv/twitter-video')], 'container': 'mp4', 'bitrate': item['bitrate']} for item in info['extended_entities']['media'][0]['video_info']['variants'] if item['content_type'] == 'video/mp4']})
				return web.json_response({'streams':[]})
		else :
			ie_result = ydl.extract_info(url, download = False)
			#return web.json_response(ie_result)
			streams = []
			for item in ie_result['formats'] :
				item_to_append = {
					'src': [item['url']],
					'tbr': item['tbr'],
					'id': item['format_id'],
					'container': item['container'] if 'container' in item else '',
					'quality': item['format_note'],
				}
				if item['acodec'] != 'none' :
					item_to_append['acodec'] = item['acodec']
				if item['vcodec'] != 'none' :
					item_to_append['vcodec'] = item['vcodec']
				streams.append(item_to_append)
				streams = sorted(streams, key = lambda item: -float(item['tbr']))
			ret = {'streams': streams, 'extractor': ie_result['extractor_key'], 'extra': {}}
			return web.json_response(ret)
	except Exception as e :
		import traceback
		traceback.print_exc()
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


