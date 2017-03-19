import scipy.sparse.linalg as ssl
import numpy as np
from time import time
from sklearn.decomposition import TruncatedSVD
from sklearn.utils.extmath import randomized_svd
from sklearn.feature_extraction.text import TfidfVectorizer


def convert_to_term_document(documents, min_df=0.1, max_df=0.9 ):

    # Create term-document representation
    print("Extracting features from the training dataset using a sparse vectorizer")
    t0 = time()

    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.9, stop_words='english', use_idf=True)
    X = vectorizer.fit_transform(documents)

    print("done in %.2fs" % (time() - t0))
    print("n_samples: {}, n_features: {}".format(X.shape[0], X.shape[1]))
    print("some features: {}".format(vectorizer.get_feature_names()[:5]))
    print()

    return X


def apply_svd(X, n_components=None):
    print("Performing dimensionality reduction using SVD")
    t0 = time()

    if not n_components:
        n_components = min(X.shape)

    # Vectorizer results are normalized, which makes KMeans behave as
    # spherical k-means for better results. Since LSA/SVD results are
    # not normalized, we have to redo the normalization.
    # svd = TruncatedSVD(n_components)
    # normalizer = Normalizer(copy=False)
    # lsa = make_pipeline(svd, normalizer)
    svd = TruncatedSVD(n_components)
    Y = svd.fit_transform(X)

    print("done in %fs" % (time() - t0))
    print("n_samples: {}, n_features: {}".format(Y.shape[0], Y.shape[1]))

    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(
        int(explained_variance * 100)))
    print()

    return Y


def test_svd_easy():
    A = np.random.random((20, 5))
    X = A.repeat(1000, 1)
    print("Real matrix shape: {} {}".format(A.shape[0], A.shape[1]))
    print("Fake matrix shape: {} {}".format(X.shape[0], X.shape[1]))
    print("Max k: ", min(X.shape))

    num_components = 19
    u, s, v = ssl.svds(X, k=num_components)
    # To get the output of TruncatedSVD:
    # X = u.dot(np.diag(s))

    print("Singular values:", s)


def test_with_numpy(X):
    P, D, Q = np.linalg.svd(X.todense(), full_matrices=False)
    print("Shapes of P, D, Q: ", P.shape, D.shape, Q.shape)
    X_a = np.dot(np.dot(P, np.diag(D)), Q)
    print(np.std(X.todense()), np.std(X_a), np.std(X.todense() - X_a))


def test_singular_values(X, num_components):
    # method 1
    print("Calculate singular values using svds")
    U, s, V = ssl.svds(X, num_components)
    # To get the output of TruncatedSVD:
    # X = U.dot(np.diag(s))
    print("Singular values:", s)

    # method 2
    print("Calculate singular values using randomized_svd")
    U, s, V = randomized_svd(X, num_components)
    # To get the output of TruncatedSVD:
    # X = U.dot(np.diag(s))
    print("Singular values:", s)


if __name__ == "__main__":
    test_svd_easy()
