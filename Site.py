from quart import Quart, render_template, request, jsonify
from deep_translator import GoogleTranslator
from Utils import *

import json

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')


@app.route("/detect", methods=['POST'])
async def detect():
    form = await request.data
    form = json.loads(form)

    text = form["text"]
    reponse = dict()

    reponse['news'] = fast_check_tools(text) if text.replace(" ", "") != "" else {}
    reponse['sentiment'] = sentimen_text(GoogleTranslator(source='auto', target='en').translate(text))  if text.replace(" ", "") != "" else 'Neutral'
    reponse['warning_link'] = decodex_link(text) if text.replace(" ", "") != "" else {}

    return jsonify(reponse)

app.run()
