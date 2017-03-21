from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import ward, average, complete, dendrogram
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from util import collection_reader


def custom_dendrogram(label_type='titles', linkage_method='ward'):
    """
    Plots a dendogram
    uses cosine similarity
    :param
    label_type: {'titles', 'ids'}
    linkage: {'ward', average}
    :return: None
    """

    # Read data
    books = collection_reader.read_books_from_mongo();
    documents = collection_reader.extract_corpus(books)

    # Labels
    if label_type == 'titles':
        labels = [
            "(" + book["book_id3"] + ") " +
            book["title"][:25] + ("..." if len(book["title"]) > 25 else "")
            for book in books]
    else:
        labels = [
            "(" + book["book_id3"] + ")" for book in books]

    # Create term-document representation
    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
    X = vectorizer.fit_transform(documents)

    # Cosine similarity matrix
    dist = 1 - cosine_similarity(X)

    # Define the linkage_matrix using ward clustering pre-computed distances
    if linkage_method == 'ward':
        linkage_matrix = ward(dist)
    elif linkage_method == 'average':
        linkage_matrix = average(dist)
    elif linkage_method == 'complete':
        linkage_matrix = complete(dist)
    else:
        raise Exception("Parameter linkage_method is not recognized!")

    # Calculate metrics


    # Plot dendrogram
    plt.subplots(figsize=(5, 5))  # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=labels)

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')

    print(ax["leaves"])
    print(ax["ivl"])

    # plt.tight_layout()  # show plot with tight layout
    plt.show()


if __name__ == "__main__":
    custom_dendrogram('ids', 'ward')
    custom_dendrogram('ids', 'average')
    custom_dendrogram('ids', 'complete')
