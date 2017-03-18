import collection_reader
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import ward, linkage, dendrogram
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def dendogram1():
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)

    # Create term-document representation
    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
    X = vectorizer.fit_transform(documents)

    # ward, single, complete, average, weighted, centroid, median
    linkage_matrix = linkage(X.todense(), 'ward')
    dendrogram(
        linkage_matrix,
        # truncate_mode="lastp",  # show only the last p merged clusters
        # p=40,  # show only the last p merged clusters
        show_leaf_counts=True,  # numbers in brackets are counts, others idx
        leaf_rotation=60.,
        leaf_font_size=8.,
        show_contracted=True,  # to get a distribution impression in truncated branches
    )
    plt.title('Hierarchical Clustering Dendrogram')
    plt.show()


def dendogram2():
    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)

    # Titles
    titles = [
        "(" + book["book_id3"] + ") " +
        book["title"][:25] + ("..." if len(book["title"]) > 25 else "")
        for book in books]

    # Create term-document representation
    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
    X = vectorizer.fit_transform(documents)

    # Cosine similarity matrix
    dist = 1 - cosine_similarity(X)

    # Define the linkage_matrix using ward clustering pre-computed distances
    linkage_matrix = ward(dist)

    fig, ax = plt.subplots(figsize=(15, 20))  # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles)

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')

    print(ax["leaves"])
    print(ax["ivl"])

    #plt.tight_layout()  # show plot with tight layout
    plt.show()


if __name__ == "__main__":
    dendogram2()