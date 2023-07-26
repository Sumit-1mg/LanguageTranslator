import os
from sanic import Sanic
from sanic.response import json
from sanic import response
from app.utils.lang_code import lang_code
from app.managers.find_language import Finder
from app.managers.file_translate import File_translator
from app.models.request import Request

app = Sanic("Translator")


@app.route('/')
async def index(request):
    with open(os.path.join(os.getcwd(), 'app/html/translator.html')) as f:
        a = f.read()
    return response.html(a)


@app.route('/find')
async def finding(request):
    with open(os.path.join(os.getcwd(), 'app/html/detector.html')) as f:
        a = f.read()
    return response.html(a)


@app.post('/finder')
async def find(request):
    finder = Finder()
    request_data = request.json
    translated_txt = finder.api_call(request_data)
    return json(translated_txt)


@app.post('/google_api')
async def google(request):
    request_obj = Request()
    request_data = request.json
    response_ = request_obj.request_handeler(request_data, 'google')
    return json(response_)


@app.post('/lacto_ai_api')
async def lacto(request):
    request_obj = Request()
    request_data = request.json
    response_ = request_obj.request_handeler(request_data, 'lacto')
    return json(response_)


@app.post('/rapid_api')
async def rapid(request):
    request_obj = Request()
    request_data = request.json
    response_ = request_obj.request_handeler(request_data, 'rapid')
    return json(response_)


@app.post('/file_google_api')
async def file_translate(request):
    translator = File_translator()
    request_data = request.json
    input_file = request_data['input_file']
    output_language = request_data['output_language']
    output_file = input_file.split('.')[0] + '_' + output_language + '.' + input_file.split('.')[1]
    ans = await translator.translate_file(input_file, output_file, output_language)
    return json(ans)


@app.post('/suggestion')
async def suggest(request):
    request_data = request.json
    obj = Request()
    response = obj.suggestion_handler(request_data)
    return json(response)
