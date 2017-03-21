# Based on
# http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py

from sklearn.cluster import KMeans

from util import plot_util, preprocessing_util, benchmark, collection_reader

if __name__ == "__main__":
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)

    print("{} books".format(len(documents)))
    print([book["book_id3"] for book in books])

    # Create term-document representation
    X = preprocessing_util.convert_to_term_document(documents, min_df=0.1, max_df=0.9)

    # SVD
    X = preprocessing_util.apply_svd(X, min(X.shape)-5)

    ###############################################################################
    # Do the actual clustering
    k = 5

    import matplotlib.pyplot as plt

    the_metrics = []
    for i in range(1):
        km = KMeans(n_clusters=k, verbose=False)
        #print("Clustering sparse data with {}".format(km))
        #t0 = time()
        km.fit(X)
        #print("done in %0.3fs" % (time() - t0))
        #print()

        # Metrics
        the_metrics.append(benchmark.clustering_metrics(X, km.labels_))

        # Plot:
        # create_2d_plot_for_sparse_matrix(X, km.labels_)
        plot_util.create_3d_plot_for_sparse_matrix(X, km.labels_, block=False)

    print("All the metrics: ")
    for a in the_metrics:
        print(a)

    plt.show()
    print("Done!")

