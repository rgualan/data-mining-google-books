import collection_reader
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.feature_extraction.text import TfidfVectorizer

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