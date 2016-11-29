from __future__ import division
import numpy as np
import functools
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.datasets import make_classification
from sklearn.cross_validation import train_test_split

def euclidean_distance(obs, train_data):
    return np.sqrt( np.sum((obs - train_data)**2, axis=1) )

def cosine_distance(obs, train_data):
    L1_train_data = np.apply_along_axis( np.linalg.norm, 1, train_data)
    L1_obs = np.linalg.norm(obs)
    cos_theta = np.dot( train_data, obs) / np.sqrt( L1_train_data * L1_obs)
    return cos_theta

class LL_KNearestNeighbors(object):
    def __init__(self, k, distance):
        self.k = k
        self.distance = distance
        self.X = None
        self.y = None

    def fit(self, X, y):
        self.X = X
        self.y = y
    
    def predict(self, X_test):
        dists = np.apply_along_axis( functools.partial(self.distance, train_data=self.X), 1, X_test) ## shape = (n_test, n_train)
        preds = np.apply_along_axis(self.find_pred_knn, 1, dists)
        return preds

    def find_pred_knn(self, dist):
        idx_sorted = np.argsort( dist )[:self.k]
        preds = self.y[idx_sorted]
        pred = Counter(preds).most_common(1)[0][0]
        return pred

    def score(self, X_test, y_true):
        y_pred = self.predict(X_test)
        accuracy = sum(y_true == y_pred) / len(y_true)
        return accuracy
        
    

if __name__ == '__main__':
    X, y = make_classification(n_features=4, n_redundant=0, n_informative=1,
                               n_clusters_per_class=1, class_sep=5,
                               random_state=5)
    
    X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.15, random_state=319)
    
    knn_cos = LL_KNearestNeighbors(k=3, distance=cosine_distance)
    knn_cos.fit(X_train_val, y_train_val)
    print 'LL_knn (cosine_distance): accuracy = {}'.format( knn_cos.score(X_test, y_test) )

    LLknn = LL_KNearestNeighbors(k=3, distance=euclidean_distance)
    LLknn.fit(X_train_val, y_train_val)
    print 'LL_knn (euclidean_distance): accuracy = {}'.format( LLknn.score(X_test, y_test) )

    SKknn = KNN(n_neighbors=3)
    SKknn.fit(X_train_val, y_train_val)
    y_pred_SK = SKknn.predict(X_test)
    print 'SK_knn (euclidean_distance): accuracy = {}'.format( SKknn.score(X_test, y_test) )


    ## Q4 Plot the decision boundary.
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    XX = X[:, :2]  # we only take the first two features. We could avoid this ugly slicing by using a two-dim dataset

    h = .5  # step size in the mesh
    # Create color maps
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
    n_neighbors = 3
    fig = plt.figure(figsize=(12,6))

    for idx_dist, dist_func in enumerate([euclidean_distance, cosine_distance]):
        # we create an instance of Neighbours Classifier and fit the data.
        cur_clf = LL_KNearestNeighbors(k=n_neighbors, distance = dist_func)
        cur_clf.fit(XX, y)

        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        x_min, x_max = XX[:, 0].min() - 1, XX[:, 0].max() + 1
        y_min, y_max = XX[:, 1].min() - 1, XX[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = cur_clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        ax = fig.add_subplot(1,2,idx_dist+1)
        ax.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        ax.scatter(XX[:, 0], XX[:, 1], c=y, cmap=cmap_bold)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_title("2-Class classification\n(k = %i, clf=%r)" % (n_neighbors, dist_func.func_name))

    plt.show()
