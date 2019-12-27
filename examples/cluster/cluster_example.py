from simforest.cluster import SimilarityForestCluster
import numpy as np
from sklearn.datasets import load_iris
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import sqeuclidean
from simforest.cluster import SimilarityTreeCluster, SimilarityForestCluster

X, y = load_iris(return_X_y=True)
import time
start = time.time()
csf = SimilarityForestCluster()
clusters = csf.fit_predict(X)
print(time.time() - start)
dendrogram(csf.links_)
plt.show()

pca = PCA(n_components=3, random_state=42).fit_transform(X, y)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(pca[:, 0], pca[:, 1], pca[:, 2], marker='o', c=clusters,
           s=50, alpha=0.7)
ax.set_title('Similarity Forest clusters')
plt.show()


'''ahc_clusters = AgglomerativeClustering(n_clusters=3, linkage='single').fit_predict(X)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(pca[:, 0], pca[:, 1], pca[:, 2], marker='o', c=ahc_clusters,
           s=50, alpha=0.7)
ax.set_title('AHC clusters')
plt.show()'''
