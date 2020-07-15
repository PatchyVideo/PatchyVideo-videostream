
from flask import Flask, session, request, current_app
app = Flask('VideoStream')

from ydl.YoutubeDL import YoutubeDL
ydl = YoutubeDL()
from you_get.extractors import bilibili

from json import dumps

@app.route("/", methods = ['POST'])
def entry() :
    request_json = request.get_json()
    try :
        if 'bilibili.com' in request_json['url'] :
            ret = bilibili.extract(request_json['url'], info_only = True)
            ret = {'streams': ret, 'extractor': 'BiliBili'}
            return current_app.response_class(dumps(ret) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])
        ie_result = ydl.extract_info(request_json['url'], download = False)
    except Exception as e :
        return current_app.response_class(dumps({"vs_err": repr(e)}) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])
    return current_app.response_class(dumps(ie_result) + '\n', mimetype = current_app.config['JSONIFY_MIMETYPE'])

if __name__ == '__main__' or __name__ == 'main' :
    app.run('0.0.0.0', 5006)
