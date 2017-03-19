import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D


def create_2d_plot_for_sparse_matrix(X, labels):
    # Create a visual representation of the clustering
    data2D = PCA(n_components=2).fit_transform(X)
    plt.figure()
    plt.scatter(data2D[:, 0], data2D[:, 1], c=labels)  # target
    plt.show()


def create_3d_plot_for_sparse_matrix(X, labels):
    """
    First apply PCA to obtain 3 main components
    then plots the resulting model in e dimension
    painting each book according to the label
    """

    # Apply PCA
    data3D = PCA(n_components=3).fit_transform(X)  # X.todense()

    fig = plt.figure()
    plt.clf()
    ax = Axes3D(fig, elev=48, azim=134)
    plt.cla()
    ax.scatter(data3D[:, 0], data3D[:, 1], data3D[:, 2], c=labels)

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Principal component 1')
    ax.set_ylabel('Principal component 2')
    ax.set_zlabel('Principal component 3')

    plt.show()

