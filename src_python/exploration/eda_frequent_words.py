import matplotlib.pylab as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from util import mongo_handler, collection_reader


def create_bag_of_words(document):
    # Vectorizer
    # vectorizer = CountVectorizer(input=corpus, strip_accents='unicode', lowercase=True, stop_words='english', max_df=0.8, min_df=0.2 )
    vectorizer = CountVectorizer(input=document, stop_words='english')
    return vectorizer.fit_transform(document), vectorizer


def max_n(row_data, row_indices, n):
    """
    Ref: http://stackoverflow.com/questions/31790819/scipy-sparse-csr-matrix-how-to-get-top-ten-values-and-indices
    """
    i = row_data.argsort()[-n:]
    # i = row_data.argpartition(-n)[-n:]
    i = i[::-1]
    top_values = row_data[i]
    top_indices = row_indices[i]  # do the sparse indices matter?
    return top_values, top_indices, i


def calc_top_words_per_document(sparse_matrix, vectorizer, n):
    """
    Prints and returns a list of the most frequent words per document
    :param sparse_matrix: bag of words
    :param vectorizer:
    :param n: number of top elements to obtain
    :return: list with the top N frequent words
    """
    top_values, top_indices, i = max_n(sparse_matrix.data, sparse_matrix.indices, n)

    feature_names = vectorizer.get_feature_names()

    # top = [[feature_names[top_indices[j]], top_values[j]] for j in range(0, len(top_indices))]
    top = [feature_names[top_indices[j]] for j in range(len(top_indices))]
    #print(list(reversed(top)))

    return list(reversed(top))


def plot_sparse_matrix(X):
    # It did not work probably because the y size is to small (24)
    # compared to the x size  (370491)
    print("Plot sparse matrix")
    plt.spy(X, precision=0.01, markersize=1)
    plt.show()


def discover_top_frequent_words():
    books = mongo_handler.query_books()
    corpus = collection_reader.extract_corpus(books)

    X, vectorizer = create_bag_of_words(corpus)

    print("Term-document matrix: ")
    print("Shape {} x {}".format(X.shape[0], X.shape[1]))
    print("Number of Feature names: {}".format(len(vectorizer.get_feature_names())))

    # Obtain the most frequent words per book
    N = 10
    print("Top {} words per document:".format(N))

    for j in range(len(corpus)):
        book_title = (books[j]["title"][:75] + '...') if len(books[j]["title"]) > 75 else books[j]["title"]
        print("Book {}: {}".format(books[j]['book_id3'], book_title))
        top_words = calc_top_words_per_document(X.getrow(j), vectorizer, N)
        print(top_words)
        books[j]["top10words"] = top_words

    mongo_handler.remove_book_2_collection()
    mongo_handler.insert_books_2(books)


def plot_top_words():
    books = mongo_handler.query_books()
    corpus = collection_reader.extract_corpus(books)
    n = 50

    X, vectorizer = create_bag_of_words(corpus)

    top_values, top_indices, i = max_n(X.data, X.indices, n)

    feature_names = vectorizer.get_feature_names()

    top_terms = [feature_names[top_indices[j]] for j in range(len(top_indices))]

    # print(i)
    # print(top_indices)
    # print(top_values)
    # print(top_terms)

    index = np.arange(len(top_values))
    bar_width = 0.8
    plt.bar(index, top_values, width=bar_width,
                     alpha=0.4,
                     color='b',
                     label='Top words')
    plt.xlabel('Terms')
    plt.ylabel('Frequency')
    plt.title('Most frequent words')
    plt.xticks(index, top_terms, rotation=90)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    discover_top_frequent_words()
    #plot_top_words()


