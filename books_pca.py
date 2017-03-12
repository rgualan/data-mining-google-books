import collection_reader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA, TruncatedSVD, NMF, SparsePCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt


corpus, titles, file_names = collection_reader.read_documents()  # Read the documents

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
])
X = pipeline.fit_transform(corpus)
X_dense = X.todense()


pca = PCA(n_components=2).fit(X_dense)
data2D = pca.transform(X_dense)
plt.figure(1)
plt.scatter(data2D[:, 0], data2D[:, 1])  # target

pca_svd = TruncatedSVD(n_components=2).fit(X)
data2D = pca_svd.transform(X)
plt.figure(2)
plt.scatter(data2D[:, 0], data2D[:, 1])  # target

nmf = NMF(n_components=2).fit(X)
data2D = nmf.transform(X)
plt.figure(3)
plt.scatter(data2D[:, 0], data2D[:, 1])  # target

sparse_pca = SparsePCA(n_components=2).fit(X_dense)
data2D = sparse_pca.transform(X_dense)
plt.figure(4)
plt.scatter(data2D[:, 0], data2D[:, 1])  # target





plt.show()

