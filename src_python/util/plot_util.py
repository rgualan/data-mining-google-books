import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


def create_2d_plot_for_sparse_matrix(X, labels):
    # Create a visual representation of the clustering
    data_2d = PCA(n_components=2).fit_transform(X)
    plt.figure()
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=labels)  # target
    plt.show()


def create_3d_plot_for_sparse_matrix(X, labels, block=True, show=True):
    """
    First apply PCA to obtain 3 main components
    then plots the resulting model in e dimension
    painting each book according to the label
    """

    # Apply PCA
    data_3d = PCA(n_components=3).fit_transform(X)

    fig = plt.figure()
    plt.clf()
    ax = Axes3D(fig, elev=15, azim=125)
    plt.cla()
    ax.scatter(data_3d[:, 0], data_3d[:, 1], data_3d[:, 2], 'o', c=labels, s=50)

    # ax.w_xaxis.set_ticklabels([])
    # ax.w_yaxis.set_ticklabels([])
    # ax.w_zaxis.set_ticklabels([])
    # ax.set_xlabel('Principal component 1')
    # ax.set_ylabel('Principal component 2')
    # ax.set_zlabel('Principal component 3')

    if show:
        plt.show(block=block)
