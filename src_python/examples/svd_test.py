from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix

X = sparse_random_matrix(100, 100, density=0.01, random_state=42)
svd = TruncatedSVD(n_components=5, n_iter=7, random_state=42)
svd.fit(X)
Y = svd.transform(X)
print("Shape ")
print(Y.shape)
print(svd.explained_variance_ratio_) # doctest: +ELLIPSIS
print(svd.explained_variance_ratio_.sum()) # doctest: +ELLIPSIS