from sklearn.cluster import Birch

from util import plot_util, preprocessing_util, benchmark, collection_reader

if __name__ == "__main__":
    # Read data
    books = collection_reader.read_books_from_mongo()
    documents = collection_reader.extract_corpus(books)
    print("{} books:".format(len(documents)))
    print([book["book_id3"] for book in books])
    print()

    # Create term-document representation
    X = preprocessing_util.convert_to_term_document(documents, min_df=0.1, max_df=0.9)

    # SVD
    X = preprocessing_util.apply_svd(X, min(X.shape))

    ###############################################################################
    # Do the actual clustering
    print("Clustering data")
    k = 5

    model = Birch(branching_factor=8, n_clusters=k, threshold=0.5,
                  compute_labels=True)
    model.fit(X)

    # Metrics
    benchmark.clustering_metrics(X, model.predict(X))

    # Create a 3d scatter plot of the corpus
    plot_util.create_3d_plot_for_sparse_matrix(X, model.predict(X))