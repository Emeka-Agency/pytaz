import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords

STOPWORDS_FILE = 'stopwords_list.txt'
stop_words = set(stopwords.words('french'))
with open(STOPWORDS_FILE, 'r', encoding="UTF-8") as f:
    additional_stopwords = [line.strip() for line in f]
stop_words.update(additional_stopwords)