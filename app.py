"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, Response, request
from flask_cors import CORS
from stopwords_list import stop_words
from utils import fetch_google_search_results, get_content_list, preprocess_content, remove_punctuation_and_numerics, density, extract_content_from_html, extract_title_from_html, extract_descr_from_html, extract_headings_from_html, get_url_content, filter_backlinks
import json

import logging
import urllib3


#disable all logging from urllib3

logging.getLogger("urllib3").setLevel(logging.WARNING)
urllib3.disable_warnings()

# pylint: disable=C0103
app = Flask(__name__)
CORS(app)

NB_WORDS = 75

def word_frequencies(txt: str):
    # print("word_frequencies")
    return preprocess_content(txt, stop_words)

def sanitize_text(txt: list):
    # print("sanitize_keywords_list")
    return remove_punctuation_and_numerics(txt)

def keywords_list(txt:str, nb_urls:int, nb_keywords:int):
    # print("keywords_list")
    most_common_keywords = sanitize_text(word_frequencies(txt)).most_common(nb_keywords)
    avg_frequencies = {word: freq/nb_urls + int(freq % nb_urls != 0) for word, freq in most_common_keywords}
    return [f"{word}:{freq}" for word, freq in avg_frequencies.items()]

@app.get("/keywords")
async def get_keywords(gl: str = "fr", hl: str = "fr", nb_keywords: int = NB_WORDS):
    import time
    start = time.time()
    try:
        words = request.args.get("query")
        print("query:", words)
        serper = fetch_google_search_results(words, gl, hl, num=100)
        print(f"number of urls: {len(serper)}")
        contents = get_content_list([item.get('link', None) for item in serper.get('organic', [])[:10]])
        content_urls_position = [{"index": index + 1, "url": item.get('url', None)} for index, item in enumerate(contents)]
        print(f"number of contents: {len(contents)}")
        nb_urls = len(contents)
        # print(f"extraxt backlinks")
        backlinks = filter_backlinks([item.get('link', None) for item in serper.get('organic', [])[11:100]], offset = 10)
        # print(f"Number of backlinks: {len(backlinks)}")
        # print(f"extraxt backlinks content")
        backlinks_content = get_content_list([item.get('url', None) for item in backlinks[:10]])
        print(f"number of backlinks content: {len(backlinks_content)}")
        nb_urls = len(contents)
        full_content = ' '.join([data.get('html', '') for data in contents])
        print(time.time() - start)
        response = {
            "status": "success",
            "datas": {
                "len_serper": len(serper),
                "len_contents": len(contents),
                "len_backlinks": len(backlinks),
                "len_backlinks_content": len(backlinks_content),
                "keywords_list": keywords_list(full_content, nb_urls, nb_keywords),
                "density": density(word_frequencies(full_content).most_common(nb_keywords), full_content),
                "urls": [item.get('link', None) for item in serper.get('organic', {})],
                "paa": serper['paa'],
                "related": serper.get('related', {}),
                "concurrents": [{
                    "occurences": {word: data.get('text', '').count(word) for word, freq in word_frequencies(data.get('text', '')).most_common(50)},
                    "keywords_list": keywords_list(data.get('html', None), nb_urls, nb_keywords),
                    "content": data.get('html', None),
                    "nb_words": len(data.get('text', None).split(' ')),
                    "title": data.get('title', None),
                    "descr": data.get('descr', None),
                    "headings": data.get('headings', None),
                    "snippet": [item.get('snippet', None) for item in serper.get('organic', {}) if item.get('link', None) == data.get('url', None)][0],
                    "url": data.get('url', None),
                    "position": [item.get('index', None) for item in content_urls_position if item.get('url', None) == data.get('url', None)][0],
                } for data in contents],
                "backlinks": [{
                    # "keywords_list": keywords_list(full_content, nb_urls, nb_keywords),
                    # "content": backlinks_content[index].get('html', None),
                    # "nb_words": len(backlinks_content[index].get('text', None).split(' ')),
                    "title": backlinks_content[index].get('title', None),
                    # "descr": backlinks_content[index].get('descr', None),
                    "headings": backlinks_content[index].get('headings', None),
                    "snippet": [item.get('snippet', None) for item in serper.get('organic', {}) if item.get('link', None) == backlinks_content[index].get('url', None)][0],
                    "url": backlinks_content[index].get('url', None),
                    "position": [item.get('index', None) for item in backlinks if item.get('url', None) == backlinks_content[index].get('url', None)][0],
                } for index in range(len(backlinks_content))],
                "pytime": time.time() - start
            },
        }
        return Response(
            status=200,
            response=json.dumps(response)
        )
    except Exception as e:
        # print(e)
        return Response(
            status=500,
            response=json.dumps({
                "status": "error",
                "datas": str(e)
            })
        )

@app.post("/my-content")
async def get_my_content(gl: str = "fr", hl: str = "fr"):
    try:
        url = request.get_json()['url']
        print("request:", url)
        content = get_url_content(url)
        return Response(
            status=200,
            response=json.dumps({
                "status": "success",
                "datas": content
            })
        )
    except Exception as e:
        return Response(
            status=500,
            response=json.dumps({
                "status": "error",
                "message": "testis",
                "error": str(e)
            })
        )

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8877')
    app.run(debug=False, port=server_port, host='0.0.0.0')
