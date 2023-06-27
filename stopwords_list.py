import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

# http://members.unine.ch/jacques.savoy/clef/index.html

stop_words = []

STOPWORDS_FILES = [
    'stopwords_list.txt',
    'complement_stopwords.txt',
    'savoy_fr.txt',
    'savoy_en.txt',
]

for file in STOPWORDS_FILES:
    with open(file, 'r', encoding="UTF-8") as f:
        for line in f:
            stop_words.append(line.strip())

languages = ["french", "english"]

for language in languages:
    stops = stopwords.words(language)
    for stop in stops:
        stop_words.append(stop.strip())