import matplotlib.pyplot as plt
from time import time
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
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

    for feature_number in range(10,24,4):
        print("Features: {}".format(feature_number))

        # SVD
        Y = preprocessing_util.apply_svd(X, feature_number)

        # Cosine similarity matrix
        dist = 1 - cosine_similarity(Y)

        ###############################################################################
        # Do the actual clustering
        k = 4
        ac = AgglomerativeClustering(linkage="average", n_clusters=k, affinity="cosine")

        print("Clustering sparse data with {}".format(ac))
        t0 = time()
        ac.fit(dist)
        print("done in {}".format(time() - t0))
        print()

        # Create a 3d scatter plot of the corpus
        plot_util.create_3d_plot_for_sparse_matrix(Y, ac.labels_, show=False)

    plt.show()
