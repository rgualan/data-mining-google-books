# Based on http://scikit-learn.org/stable/auto_examples/text/document_clustering.html#sphx-glr-auto-examples-text-document-clustering-py

import json
import collection_reader
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import numpy as np
from pprint import pprint

OUTPUT_FOLDER = "output/json-text-only-2"

documents = collection_reader.read_documents()

print("{} books".format(len(documents)))

print("Extracting features from the training dataset using a sparse vectorizer")

t0 = time()
vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                             min_df=2, stop_words='english',
                             use_idf=True)
X = vectorizer.fit_transform(documents)

print("done in %fs" % (time() - t0))
print("n_samples: {}, n_features: {}".format(X.shape[0],X.shape[1]))
print()

###############################################################################
# Do the actual clustering
k = 10

km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1,
            verbose=True)

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
