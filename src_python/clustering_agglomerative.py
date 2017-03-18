import collection_reader
import plot_util
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering

if __name__ == "__main__":
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)
    print("{} books:".format(len(documents)))
    print([book["book_id3"] for book in books])
    print()

    # Create term-document representation
    print("Extracting features from the training dataset using a sparse vectorizer")
    t0 = time()
    # vectorizer = TfidfVectorizer(min_df=0.3, max_df=0.9, stop_words='english', use_idf=True)
    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
    X = vectorizer.fit_transform(documents)

    print("done in %.2fs" % (time() - t0))
    print("n_samples: {}, n_features: {}".format(X.shape[0], X.shape[1]))
    print()

    print(X)

    ###############################################################################
    # Do the actual clustering
    k = 5

    # linkage: ward, average, complete
    # affinity: cosine, euclidean, cityblock
    ac = AgglomerativeClustering(linkage="ward", n_clusters=k, affinity="euclidean")

    print("Clustering sparse data with {}".format(ac))
    t0 = time()
    ac.fit(X.todense())
    print("done in {}".format(time() - t0))
    print()

    print("Cluster results:")
    print(ac.labels_)

    # Create a 3d scatter plot of the corpus
    plot_util.create_3d_plot_for_sparse_matrix(X, ac.labels_)

