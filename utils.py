import json
import requests
import trafilatura
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import concurrent.futures
import string
from bs4 import BeautifulSoup


API_KEY = 'eccc0d4e0381f0384b60f9b7409529e9c6e12f13'
CONTENT_TYPE = 'application/json'


def fetch_google_search_results(query: str, gl: str, hl: str) -> dict:
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': API_KEY, 'Content-Type': CONTENT_TYPE}
    payload = json.dumps({"q": query, "gl": gl, "hl": hl})
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
    except:
        print(f"can't get content from url: {url}")
        return None



def get_content_list(urls: list) -> list:
    contents = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
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
        print(e)
        return "Pas de description"

def extract_headings_from_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    return [{"type": heading.name, "text": heading.text} for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]