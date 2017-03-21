import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import TruncatedSVD, PCA, NMF, SparsePCA
from sklearn.feature_extraction.text import TfidfVectorizer
from util import collection_reader
from clustering.potential_labels import test_labels


def create_2d_plot(data_2d, p):
    plt.figure()
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=test_labels)
    plt.title("min_df {:.2f}, max_df {:.2f}".format(p[0], p[1]))


def create_3d_plot(data_3d, p):
    fig = plt.figure()
    plt.clf()
    ax = Axes3D(fig, elev=15, azim=125)
    plt.cla()
    ax.scatter(data_3d[:, 0], data_3d[:, 1], data_3d[:, 2], 'o', c=test_labels, s=50)
    plt.title("min_df {:.2f}, max_df {:.2f}".format(p[0], p[1]))


def test_svd():
    corpus = collection_reader.read_books_corpus()  # Read the documents

    params = [[0.1, 0.9],
              [0.2, 0.8],
              [0.3, 0.7],
              [0.4, 0.6]]

    for p in params:
        # vectorizer = TfidfVectorizer(corpus, min_df=0.30, max_df=0.70)
        print("testing with min_df {:.2f} and max_df {:.2f}".format(p[0], p[1]))
        vectorizer = TfidfVectorizer(corpus, min_df=p[0], max_df=p[1])
        X = vectorizer.fit_transform(corpus)
        print("Shape: {} {}".format(X.shape[0], X.shape[1]))

        ###############################################################
        # PCA
        # 2D-plot
        # data_2d = PCA(n_components=2).fit_transform(X.todense())
        # create_2d_plot(data_2d, p)

        # 3D-plot
        # data_3d = PCA(n_components=3).fit_transform(X.todense())
        # create_3d_plot(data_3d, p)

        ###############################################################
        # TruncatedSVD
        # 2D plot
        # data_2d = TruncatedSVD(n_components=2).fit_transform(X)
        # create_2d_plot(data_2d, p)

        # 3D plot
        # data_3d = TruncatedSVD(n_components=3).fit_transform(X)
        # create_3d_plot(data_3d, p)

        ###############################################################
        # NMF
        # 2D plot
        # data_2d = NMF(n_components=2).fit_transform(X)
        # create_2d_plot(data_2d, p)

        # 3D plot
        data_3d = NMF(n_components=3).fit_transform(X)
        create_3d_plot(data_3d, p)

        ###############################################################
        # SparsePCA
        # 2D plot
        # data_2d = SparsePCA(n_components=2).fit_transform(X.todense())
        # create_2d_plot(data_2d, p)

        # 3D plot
        # data_3d = SparsePCA(n_components=3).fit_transform(X.todense())
        # create_3d_plot(data_3d, p)

    plt.show()


if __name__ == "__main__":
    test_svd()
