from quart import Quart, render_template, request
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

    reponse['news'] = fast_check_tools(text)
    reponse['sentiment'] = sentimen_text(text)
    reponse['warning_link'] = decodex_link(text)

    return str(reponse)

app.run()
