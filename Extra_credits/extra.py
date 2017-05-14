from sklearn.neighbors import KDTree
import numpy as np
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.neighbors import KDTree
from sklearn import datasets
from collections import Counter




class Knn:
    def __init__(self, X, y, k):
        self.x = X
        self.k = k
        self.labels = y

    def predict(self, data_point):
        output = []

        def is_alpha(obj):
            attrs = ['[a-zA-Z]']
            return all(hasattr(obj, attr) for attr in attrs)

        #print 'j'
        if is_alpha(self.x):
            # for categorical variables
            #print 'i'
            temp = KNeighborsClassifier(n_neighbors=self.k, algorithm='kd_tree')
            temp.fit(self.x, self.labels)
            output = temp.predict(data_point)
            value = Counter(self.labels)

        for points in output:
            p_probability = value[points] / self.k
            final_output = (points, p_probability)
            print final_output

        else:
            # for numeric variables
            #print'f'
            temp = KNeighborsRegressor(n_neighbors=self.k, algorithm='kd_tree')
            temp.fit(self.x, self.labels)
            output = temp.predict(data_point)
            dist, ind = temp.kneighbors(data_point, n_neighbors=self.k, return_distance=True)

        for points, elements in zip(output, dist):
            mean_value = np.mean(elements)
            max_sum = 0
            for element in elements:
                max_sum = max_sum + ((element - mean_value) / self.k)
            final_output = (mean_value, max_sum)
            print final_output

iris = datasets.load_iris()
train = iris.data
labels=iris.target

a = datasets.load_boston()
b = a.data
c = a.target
X = [train]
d = np.array(X)
pred = train[:1]
predic = b[:1]
final_value = Knn(b, c, 3)
final_value.predict(predic)
