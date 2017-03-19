# Based on
# http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py

import collection_reader
import plot_util
import preprocessing_util
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


if __name__ == "__main__":
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)

    print("{} books".format(len(documents)))
    print([book["book_id3"] for book in books])

    # Create term-document representation
    X = preprocessing_util.convert_to_term_document(documents, min_df=0.1, max_df=0.9)

    # SVD
    X = preprocessing_util.apply_svd(X, min(X.shape))

    ###############################################################################
    # Do the actual clustering
    k = 4

    km = KMeans(n_clusters=k, verbose=False)
    print("Clustering sparse data with {}".format(km))
    t0 = time()
    km.fit(X)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Resulting labels: {}".format(km.labels_))
    print()

    # Plot:
    plot_util.create_3d_plot_for_sparse_matrix(X, km.labels_)
    # plot_util.create_2d_plot_for_sparse_matrix(X, km.labels_)
