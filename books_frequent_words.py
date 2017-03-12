import collection_reader
from sklearn.feature_extraction.text import CountVectorizer


corpus, titles, file_names = collection_reader.read_documents()  # Read the documents

# Vectorizers
#vectorizer = CountVectorizer(input=corpus, strip_accents='unicode', lowercase=True, stop_words='english', max_df=0.8, min_df=0.2 )
vectorizer = CountVectorizer(input=corpus, strip_accents='unicode', lowercase=True, stop_words='english' )

# Create bag of words
X = vectorizer.fit_transform(corpus)

#print("term-document matrix")
#print(X)

print("Shape"); print(X.shape)
print("Number of Feature names: "); print(len(vectorizer.get_feature_names()))
#print("Stop words"); print(vectorizer.get_stop_words())

# Obtain the most frequent words per book
print("Top words per book")


def max_n(row_data, row_indices, n):
    """ Ref: http://stackoverflow.com/questions/31790819/scipy-sparse-csr-matrix-how-to-get-top-ten-values-and-indices
    """
    i = row_data.argsort()[-n:]
    # i = row_data.argpartition(-n)[-n:]
    top_values = row_data[i]
    top_indices = row_indices[i]  # do the sparse indices matter?
    return top_values, top_indices, i


def top_words_per_document(sparse_matrix, vectorizer, n):
    top_values, top_indices, i =  max_n(sparse_matrix.data, sparse_matrix.indices, n)

    feature_names = vectorizer.get_feature_names()

    top =  [[feature_names[top_indices[j]], top_values[j] ] for j in range(0,len(top_indices))]
    print(top)

    return top


print("Top words per document:")
N = 10
for j in range(24):
    print("{} >>> {}".format(file_names[j], titles[j]))
    top_words_per_document(X.getrow(j), vectorizer, N)


print("Plot sparse matrix")

import matplotlib.pylab as plt
import scipy.sparse as sps
plt.spy(X, precision=0.01, markersize=1)
plt.show()
