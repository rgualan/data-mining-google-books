import collection_reader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.decomposition import PCA, TruncatedSVD, NMF, SparsePCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt


corpus = collection_reader.read_books_corpus()  # Read the documents

# pipeline = Pipeline([
#     ('vect', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
# ])
# X = pipeline.fit_transform(corpus)
# X_dense = X.todense()

vectorizer = TfidfVectorizer(corpus, min_df=0.30, max_df=0.70 )
X = vectorizer.fit_transform(corpus)
X_dense = X.todense()


# pca = PCA(n_components=2).fit(X_dense)
# data2D = pca.transform(X_dense)
# plt.figure(1)
# plt.scatter(data2D[:, 0], data2D[:, 1])  # target

pca_svd = TruncatedSVD(n_components=2).fit(X)
data2D = pca_svd.transform(X)
plt.figure(2)
plt.scatter(data2D[:, 0], data2D[:, 1])  # target

# nmf = NMF(n_components=2).fit(X)
# data2D = nmf.transform(X)
# plt.figure(3)
# plt.scatter(data2D[:, 0], data2D[:, 1])  # target

# sparse_pca = SparsePCA(n_components=2).fit(X_dense)
# data2D = sparse_pca.transform(X_dense)
# plt.figure(4)
# plt.scatter(data2D[:, 0], data2D[:, 1])  # target

#plt.show()


##########################################################
# Create a 3d scatter plot of the corpus

# Apply PCA
# pca = PCA(n_components=3).fit(X_dense)
# data3D = pca.transform(X_dense)
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# plt.clf()
# ax = Axes3D(fig, elev=48, azim=134)
# plt.cla()
# ax.scatter(data3D[:, 0], data3D[:, 1], data3D[:, 2] )

plt.show()
