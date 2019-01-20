from sklearn import neighbors
import numpy as np


NUM_NEIGHBORS = 1
L_DISTANCE = 2

# clf = neighbors.KNeighborsClassifier(NUM_NEIGHBORS, p=L_DISTANCE)
# clf.fit(x_train, y_train)

class Voice_Rec(object):
    def __init__(self, x_train, y_train):
        self.clf = neighbors.KNeighborsClassifier(NUM_NEIGHBORS, p=L_DISTANCE)
        self.clf.fit(x_train, y_train)

    def predict(self, x):
        return self.clf.predict(x)

if __name__ == "__main__":

    # Import our audio library
    x_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([1, 1, 2, 2])
    print(x_train.shape)
    print(y_train.shape)
    mine = Voice_Rec(x_train, y_train)
    print(mine.predict(np.array([[3]])))
