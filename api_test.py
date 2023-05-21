import uvicorn
from fastapi import FastAPI, Response
from typing import List
import seaborn as sns
import matplotlib.pyplot as plt
from stopwords_list import stop_words
from utils import fetch_google_search_results, get_content_list, preprocess_content, remove_punctuation_and_numerics, density, extract_content_from_html, extract_title_from_html, extract_descr_from_html, extract_headings_from_html
from fastapi.middleware.cors import CORSMiddleware
import json

NB_WORDS = 75

app = FastAPI()
origins = [
    # "https://taz.kevinlesieutre.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def get_keywords(query: str, gl: str = "fr", hl: str = "fr", nb_keywords: int = NB_WORDS):
    try:
        print("query:", query)
        serper = fetch_google_search_results(query, gl, hl)
        print(f"number of urls: {len(serper)}")
        contents = get_content_list([item.get('link', None) for item in serper.get('organic', {})])
        print(f"number of contents: {len(contents)}")
        nb_urls = len(contents)
        full_content = ' '.join([data.get('html', '') for data in contents])
        return Response(
            status_code=200,
            content=json.dumps({
                "status": "success",
                "datas": {
                    "keywords_list": keywords_list(full_content, nb_urls, nb_keywords),
                    "density": density(word_frequencies(full_content).most_common(nb_keywords), full_content),
                    "urls": [item.get('link', None) for item in serper.get('organic', {})],
                    "paa": serper['paa'],
                    "related": serper.get('related', {}),
                    "concurrents": [{
                        "keywords_list": keywords_list(full_content, nb_urls, nb_keywords),
                        # "density": density(word_frequencies(data.get('html', '')).most_common(nb_keywords), data.get('html', '')),
                        "content": data.get('html', None),
                        "nb_words": len(data.get('content', None).split(' ')),
                        "title": data.get('title', None),
                        "descr": data.get('descr', None),
                        "headings": data.get('headings', None),
                        "url": data.get('url', None),
                    } for data in contents]
                }
            })
        )
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        return Response(
            status_code=500
        )
        


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)
    
    
    
    
    

