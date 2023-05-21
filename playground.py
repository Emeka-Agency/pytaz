import seaborn as sns
import matplotlib.pyplot as plt
from stopwords_list import stop_words
from utils import fetch_google_search_results, get_content_list, preprocess_content, remove_punctuation_and_numerics, save_keywords_to_file


WORD_LIST_FILE = 'word_list.txt'
QUERY = "avocat rgpd"
GL = "fr"
HL = "fr"
NUM_KEYWORDS = 50


def main() -> None:
    urls = fetch_google_search_results(QUERY, GL, HL)
    contents = get_content_list(urls)
    num_urls = len(contents)
    word_frequencies = preprocess_content(contents, stop_words)
    remove_punctuation_and_numerics(word_frequencies)
    most_common_keywords = word_frequencies.most_common(NUM_KEYWORDS)
    avg_frequencies = {word: freq//num_urls + int(freq % num_urls != 0) for word, freq in most_common_keywords}
    save_keywords_to_file([f"{word}:{freq}" for word, freq in avg_frequencies.items()], WORD_LIST_FILE)
    sns.set(rc={'figure.figsize':(13,8)})
    sns.barplot(
        x=[freq for _, freq in avg_frequencies.items()],
        y=list(avg_frequencies),
    )
    plt.xticks(rotation=90)
    plt.show()


if __name__ == '__main__':
    main()


    # save_keywords_to_file([f"{word}:{freq}" for word, freq in avg_frequencies.items()], word_list_file)
    # word_list_file = f"{query}_word_list.txt"
    # sns.set(rc={'figure.figsize':(13,8)})
    # sns.barplot(
    #     x=[freq for _, freq in avg_frequencies.items()],
    #     y=list(avg_frequencies),
    # )
    # plt.xticks(rotation=90)
    # plt.savefig(f'{query}_keywords_graph.png')