# Based on http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py

import collection_reader
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

documents = collection_reader.read_books_corpus()

print("{} books".format(len(documents)))

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()
#vectorizer = TfidfVectorizer(min_df=0.3, max_df=0.9, stop_words='english', use_idf=True)
vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
X = vectorizer.fit_transform(documents)

print("done in %fs" % (time() - t0))
print("n_samples: {}, n_features: {}".format(X.shape[0],X.shape[1]))
print()

###############################################################################
# Do the actual clustering
k = 4

km = KMeans(n_clusters=k, verbose=False)

print("Clustering sparse data with {}".format(km))
t0 = time()
km.fit(X)
print("done in %0.3fs" % (time() - t0))
print()

print("For calculating some metrics it is necessary to have the labels. But I don't have such information")
print("Resulting labels: {}".format(km.labels_))
print()

print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :20]:
        print(' %s' % terms[ind], end='')
    print()


##########################################################
# Create a visual representation of the clustering
# pca = PCA(n_components=2).fit(X.todense())
# data2D = pca.transform(X.todense())
# plt.figure()
# plt.scatter(data2D[:, 0], data2D[:, 1], c=km.labels_)  # target
# plt.show()

##########################################################
# Create a 3d scatter plot of the corpus

# Apply PCA
pca = PCA(n_components=3).fit(X.todense())
data3D = pca.transform(X.todense())

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
plt.clf()
ax = Axes3D(fig, elev=48, azim=134)
plt.cla()
ax.scatter(data3D[:, 0], data3D[:, 1], data3D[:, 2], c=km.labels_ )
plt.show()
