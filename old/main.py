import json
import requests
import trafilatura
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import plotly.express as px
import string
import concurrent.futures

API_KEY = 'eccc0d4e0381f0384b60f9b7409529e9c6e12f13'
CONTENT_TYPE = 'application/json'
STOPWORDS_FILE = 'stopwords_list.txt'
WORD_LIST_FILE = 'word_list.txt'

def fetch_google_search_results(query: str, gl: str, hl: str) -> dict:
    url = "https://google.serper.dev/search"
    headers = {'X-API-KEY': API_KEY, 'Content-Type': CONTENT_TYPE}
    payload = json.dumps({"q": query, "gl": gl, "hl": hl})
    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text)

def extract_urls_from_search_result(search_result: dict) -> list:
    return [item['link'] for item in search_result['organic']]

def get_content(url: str) -> str:
    content = trafilatura.fetch_url(url)
    return trafilatura.extract(content)

def get_content_list(urls: list) -> list:
    contents = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(get_content, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                content = future.result()
                contents.append(content)
            except Exception:
                print(f"can't get content from url: {url}")
    return contents

def preprocess_content(contents: list, stop_words: set) -> FreqDist:
    filtered_tokens = [
        token for token in word_tokenize(' '.join(contents))
        if token.lower() not in stop_words
    ]
    return FreqDist(filtered_tokens)

def remove_punctuation_and_numerics(word_frequencies: FreqDist) -> None:
    for word in list(word_frequencies):
        if word in string.punctuation or not word.isalpha():
            del word_frequencies[word]

def save_keywords_to_file(keywords: list, filename: str) -> None:
    with open(filename, 'w',encoding="UTF-8") as f:
        f.write(' '.join(keywords))

def plot_treemap(word_frequencies: FreqDist) -> None:
    data = {"Word": [], "Frequency": []}
    for word, freq in word_frequencies.items():
        data["Word"].append(word)
        data["Frequency"].append(freq)

    fig = px.treemap(data, path=["Word"], values="Frequency", title="Treemap of Word Frequencies")
    fig.show()
    
def main() -> None:
    google_search_result = fetch_google_search_results("avocat rgpd", "fr", "fr")
    urls = extract_urls_from_search_result(google_search_result)
    contents = get_content_list(urls)
    stop_words = set(stopwords.words('french'))
    with open(STOPWORDS_FILE, 'r', encoding="UTF-8") as f:
        additional_stopwords = [line.strip() for line in f]
    stop_words.update(additional_stopwords)
    word_frequencies = preprocess_content(contents, stop_words)
    remove_punctuation_and_numerics(word_frequencies)
    most_common_keywords = word_frequencies.most_common(50)
    save_keywords_to_file([word for word, _ in most_common_keywords], WORD_LIST_FILE)
    word_frequencies = FreqDist(dict(most_common_keywords))
    plot_treemap(word_frequencies)


if __name__ =="__main__":
    main()