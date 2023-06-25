import json
import requests
import trafilatura
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import concurrent.futures
import string
from bs4 import BeautifulSoup

from const import API_KEY, CONTENT_TYPE, PATTERNS

def fetch_google_search_results(query: str, gl: str, hl: str, num: int = 10) -> dict:
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': API_KEY, 'Content-Type': CONTENT_TYPE}
    payload = json.dumps({"q": query, "gl": gl, "hl": hl, "num": num, "autocorrect": False})
    response = requests.post(url, headers=headers, data=payload)
    response = json.loads(response.text)
    return {
        "organic": [item for item in response.get('organic', [])],
        "paa": [item for item in response.get('peopleAlsoAsk', [])],
        "related": [item for item in response.get('relatedSearches', [])],
    }

def get_content(url: str) -> str:
    try:
        return trafilatura.fetch_url(url)
        # return trafilatura.fetch_url(url, http_headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        # return requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3).text
    except trafilatura.TrafilaturaException:
        print(f"Can't get content from URL: {url}")
        return None
    except:
        print(f"can't get content from url: {url}")
        return None

def get_url_content(url:str) -> str:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_content, url)
        try:
            content = future.result()
            if content is not None:
                return {
                    "content": content,
                    "url": url,
                    "text": trafilatura.extract(content, include_images=False),
                    "html": trafilatura.extract(content),
                    "title": extract_title_from_html(content),
                    "descr": extract_descr_from_html(content),
                    "headings": extract_headings_from_html(content), 
                }
            else:
                # print(f"can't get content from url")
                return {
                "status": "error",
                "message": "else"
            }
        except Exception as e:
            # print(e)
            # print(f"can't get content from url")                                                  
            return {
                "status": "error",
                "message": str(e)
            }

def get_content_list(urls: list) -> list:
    contents = []
    num_workers = 10
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_url = {executor.submit(get_content, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                content = future.result()
                if content is not None:
                    contents.append({
                        "content": content,
                        "url": url,
                        "text": trafilatura.extract(content, include_images=False),
                        "html": trafilatura.extract(content),
                        "title": extract_title_from_html(content),
                        "descr": extract_descr_from_html(content),
                        "headings": extract_headings_from_html(content), 
                    })
                else:
                    print(f"can't get content from url: {url}")
            except Exception:
                print(f"can't get content from url: {url}")
    return contents

def filter_backlinks(backlinks: list, patterns: list = PATTERNS, offset: int = 0) -> list:
    return [{"index": index + offset + 1, "url": backlinks[index]} for index in range(0, len(backlinks)) if any(pattern in backlinks[index] for pattern in patterns)]

def preprocess_content(contents: list, stop_words: set) -> FreqDist:
    filtered_tokens = [
        token.lower() for token in word_tokenize(contents)
        if token.lower() not in stop_words and token.isalpha()
    ]

    return FreqDist(filtered_tokens)


def remove_punctuation_and_numerics(word_frequencies: FreqDist) -> str:
    for word in list(word_frequencies):
        if word in string.punctuation or not word.isalpha():
            del word_frequencies[word]
    return word_frequencies


def density(most_common_keywords: any, content: str) -> dict:
    return {word: float(content.count(word)/len(content.split(' '))) for word, freq in most_common_keywords}

def extract_content_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def extract_title_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string

def extract_descr_from_html(html: str) -> str:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find("meta",  property="og:description").get("content", None)
    except Exception as e:
        # print(e)
        return "Pas de description"

def extract_headings_from_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    return [{"type": heading.name, "text": heading.text} for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]