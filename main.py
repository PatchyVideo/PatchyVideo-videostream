
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

from bson.json_util import dumps, loads

from aiohttp import web
from aiohttp import ClientSession

from you_get.extractors import bilibili

app = web.Application()
routes = web.RouteTableDef()

@routes.post("/")
async def entry(request) :
	try :
		url = (await request.json())['url']
		if 'bilibili.com' in url :
			extractor_instance = bilibili.Bilibili()
			info = await extractor_instance.extract_info_only(url, info_only = True)
			extra_info = {}
			if hasattr(extractor_instance, 'video_cid') :
				extra_info['cid'] = extractor_instance.video_cid
			if hasattr(extractor_instance, 'lyrics') :
				extra_info['lyrics'] = extractor_instance.lyrics
			if hasattr(extractor_instance, 'danmaku') :
				extra_info['danmaku'] = extractor_instance.danmaku
			ret = {'streams': info, 'extractor': 'BiliBili', 'extra': extra_info}
			return web.json_response(ret, dumps = dumps)
	except Exception as e :
		return web.json_response({"vs_err": repr(e)}, dumps = dumps)

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


