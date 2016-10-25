from __future__ import division
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans as skKMeans
from matplotlib import pyplot as plt
import numpy as np
import random
from sklearn.metrics import silhouette_score

class KMeans(object):
    def __init__(self):
        pass

    def fit(self, data, k=10, max_iter=100):
        ## randomly assign the initialization values
        self.centers = np.array( random.sample(data, k) ) 
        prev_labels_kmeans = np.ones(data.shape[0])

        ## run max_iter iterations or
        ## no cluster assignments change between iterations
        for idx_iter in xrange(max_iter):
            labels_kmeans = np.apply_along_axis(self._get_closest_center, 1, data)
            self.centers = get_centers(data, labels_kmeans)
            is_no_labels_kmeans_change = (sum(prev_labels_kmeans!=labels_kmeans)==0)
            if is_no_labels_kmeans_change:
                break
            else:
                prev_labels_kmeans = labels_kmeans
        return self.centers, labels_kmeans

    def _get_closest_center(self, obs):
        ## calcualte euclidean distance
        dists = np.sum((obs - self.centers)**2, axis=1)
        idx_dists = dists.argsort()
        return idx_dists[0]

    def plot_k_elbow_mthd(self, data, min_k, max_k, ax):
        print 'Elbow method'
        scores = []
        ks = range(min_k, max_k+1)
        for k in ks:
            print k
            centers, clusters = self.fit(data, k=k)
            scores.append( get_sse(data, centers, clusters) )
        ax.plot(ks, scores, marker='o', ls='-')
        ax.set_xlabel('"k" in k-means')
        ax.set_ylabel('sum of squared error\n(the lower the better)')
        ax.set_title('Elbow method')

    def plot_k_silhouette_mthd(self, data, min_k, max_k, ax):
        print 'Silhouette method'
        scores = []
        ks = range(min_k, max_k+1)
        for k in ks:
            print k
            centers, clusters = self.fit(data, k=k)
            scores.append( silhouette_score(data, clusters, metric='euclidean'))
        ax.plot(ks, scores, marker='o', ls='-')
        ax.set_xlabel('"k" in k-means')
        ax.set_ylabel('silhouette score\n(the lower the better)')
        ax.set_title('Silhouette method')


def get_sse(data, centers, clusters):
    target_centers = np.array(centers)[clusters]
    squared_error = np.sum((target_centers - data)**2, axis=1)
    return sum(squared_error)

def plot_data_kmeans(data, ax, labels=None, centers=None, fnames=None):
    x_idx = 0
    y_idx = 1
    if labels is None:
        ax.scatter(data[:,x_idx], data[:,y_idx])
    else:
        ax.scatter(data[:,x_idx], data[:,y_idx], c=labels+1)
        if centers is not None:
            ax.scatter(centers[:,x_idx], centers[:,y_idx], marker='x', color=np.arange(len(centers))+1, s=50)
    if fnames is not None:
        ax.set_xlabel( fnames[x_idx])
        ax.set_ylabel( fnames[y_idx])

def get_centers(data, labels):
    centers = np.empty([ len(set(labels)), data.shape[1]])
    for cc in set(labels):
        cur_data = data[labels==cc]
        if cur_data.shape[0]>0:
            cur_center = np.mean(cur_data, axis=0)
            centers[cc] = cur_center
    return centers

if __name__ == '__main__':
    data_all = load_iris()
    data = data_all.data
    fnames = data_all.feature_names
    mdl = KMeans()

    fig = plt.figure(1, figsize=(12,8))
    
    ## k-mean clusters for choosing "k"
    ax = fig.add_subplot(2,2,1)
    mdl.plot_k_elbow_mthd(data, 2, 10, ax=ax)
    ax = fig.add_subplot(2,2,2)
    mdl.plot_k_silhouette_mthd(data, 2, 10, ax=ax)
    centers, labels_my_cluster = mdl.fit(data, k=3, max_iter=1000)
    
    plt.tight_layout()

    ## comparison of k-means cluster and its performance
    ## my k-mean cluster
    ax = fig.add_subplot(2,3,4)
    plot_data_kmeans(data, ax=ax, labels=labels_my_cluster, centers=centers, fnames=fnames)
    ax.set_title('My K-mean clustering')
    
    ## sklearn k-mean cluster
    labels_sk = skKMeans(n_clusters=3).fit(data).labels_
    centers_sk = get_centers(data, labels_sk)
    ax = fig.add_subplot(2,3,5)
    plot_data_kmeans(data, ax=ax, labels=labels_sk, centers=centers_sk, fnames=fnames)
    ax.set_title('sklearn\'s K-mean clustering')

    ## truth
    ax = fig.add_subplot(2,3,6)
    labels_true = data_all.target
    centers_true = get_centers(data, labels_true)
    plot_data_kmeans(data, ax=ax, labels=labels_true, centers=centers_true, fnames=fnames)
    ax.set_title('Truth')

    plt.show()
        


