from monkeylearn import MonkeyLearn

import requests
import json
import re

f = open('data/updates.json')

decodex = json.load(f)
ml = MonkeyLearn('c868fd48f12ff2bb4a182b45af1ea2c21f55e80e')


def find_url(text: str) -> list:
    _urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    _uri = []

    for i in _urls:
        _url = (i.split("/")[2]+"/"+i.split("/")[3]).replace("www.", "", 1)
        if _url [-1] == "/":
            _url = _url[:-1]

        _uri.append(_url)

    return _uri


def sentimen_text(text: str) -> str:

    for i in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
        text = text.replace(i, "")

    data = [text]

    model_id = 'cl_pi3C7JiL'
    result = ml.classifiers.classify(model_id, data)

    return result.body[0]['classifications'][0]['tag_name']


def decodex_link(text: str) -> dict:
    _url = find_url(text)

    value = dict()

    for uri in _url:
        for i, item in decodex['urls'].items():
            if i == uri:
                value[uri] = decodex['sites'][str(item)][1]

    return value


def fast_check_tools(text: str) -> dict:
    for i in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
        text = text.replace(i, "")
    response = requests.get(url='https://factchecktools.googleapis.com/v1alpha1/claims:search', params=dict(
        key='AIzaSyAGZVW9V24uNcW8Yj-rQPdLFv7qwgCKwCM',
        query=text)
    )

    data = json.loads(response.text)

    current = {}

    if 'claims' not in data:
        return {}

    for i, item in enumerate(data['claims']):
        if i <= 2:
            current[f'response_{i}'] = \
                [data['claims'][i]['text'], data['claims'][i]['claimReview'][0]['title'], data['claims'][i]['claimReview'][0]['url'], data['claims'][i]['claimReview'][0]['textualRating']]

    return current
