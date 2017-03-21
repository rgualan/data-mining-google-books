from sklearn import metrics
from src_python.clustering.potential_labels import true_labels


def clustering_metrics(X, labels):
    """
    Calculate some performance metrics to assess the clustering techniques
    :param X: document-term matrix
    :param labels:
    """

    print("Clusters:")
    print("True labels    : ", true_labels)
    print("Cluster Labels : ", labels.tolist())
    print()

    m = [metrics.homogeneity_score(true_labels, labels),
         metrics.completeness_score(true_labels, labels),
         metrics.v_measure_score(true_labels, labels),
         metrics.adjusted_rand_score(true_labels, labels),
         metrics.silhouette_score(X, labels, sample_size=1000)]

    print("Performance Metrics: ")
    print("Homogeneity: %0.3f" % m[0])
    print("Completeness: %0.3f" % m[1])
    print("V-measure: %0.3f" % m[2])
    print("Adjusted Rand-Index: %.3f" % m[3])
    print("Silhouette Coefficient: %0.3f" % m[4])
    print()

    return m
