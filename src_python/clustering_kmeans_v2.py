# Based on
# http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py

import collection_reader
import plot_util
import decomposition_util
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
    print("Extracting features from the training dataset using a sparse vectorizer")
    t0 = time()
    # vectorizer = TfidfVectorizer(min_df=0.3, max_df=0.9, stop_words='english', use_idf=True)
    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.9, stop_words='english', use_idf=True)
    X = vectorizer.fit_transform(documents)

    print("done in %.2fs" % (time() - t0))
    print("n_samples: {}, n_features: {}".format(X.shape[0], X.shape[1]))
    print("some features: {}".format(vectorizer.get_feature_names()[:20]))
    print()

    #import decomposition_util
    #decomposition_util.test_singular_values(X, 20) #k between 1 and min(X.shape)

    # SVD
    X = decomposition_util.apply_svd(X, min(X.shape))

    ###############################################################################
    # Do the actual clustering
    k = 6

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
