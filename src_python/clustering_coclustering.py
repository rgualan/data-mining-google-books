import collection_reader
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster.bicluster import SpectralCoclustering
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

documents = collection_reader.read_books_corpus()  # Read data
print("{} books".format(len(documents)))

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()
#vectorizer = TfidfVectorizer(min_df=0.3, max_df=0.9, stop_words='english', use_idf=True)
vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7, use_idf=True)
X = vectorizer.fit_transform(documents)
Xdense = X.todense()
print("done in %fs" % (time() - t0))
print("n_samples: {}, n_features: {}".format(X.shape[0],X.shape[1]))
print()

###############################################################################
# Do the actual clustering
k = 5

print("Clustering sparse data")
t0 = time()

#linkage: ward, average, complete
# affinity: cosine, euclidean, cityblock
#model = SpectralCoclustering(n_clusters=k, svd_method='arpack', random_state=0)
model = SpectralCoclustering(n_clusters=k, svd_method='arpack', random_state=0)
model.fit(X)
print("done in %0.3fs \n" % (time() - t0))

print("Row labels: {}".format(len(np.unique(model.row_labels_))))
print(model.row_labels_)
print("Column labels: {}".format(len(np.unique(model.column_labels_))))
#print(model.column_labels_)


# print("Top terms per cluster:")
# order_centroids = ac.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(k):
#     print("Cluster %d:" % i, end='')
#     for ind in order_centroids[i, :20]:
#         print(' %s' % terms[ind], end='')
#     print()


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
ax.scatter(data3D[:, 0], data3D[:, 1], data3D[:, 2], c=model.row_labels_)
plt.show()
