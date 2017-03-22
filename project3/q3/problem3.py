import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
#from sklearn.svm import SVC
#from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing
from sklearn import svm, grid_search
from sklearn import linear_model
from sklearn import neighbors
from sklearn import tree
from sklearn import ensemble

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    h = 0.2  # Step size in the mesh

    # Put the data into Python lists
    df = pd.read_csv(input_file, names=['A', 'B', 'label'])
    arr =  np.asarray(df)
    arr = arr[1:]

    X = arr[:,:2].astype(float)
    y = arr[:, 2].astype(int)

    # Standardize the data
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=0, stratify=y)


    x_min, x_max = X[:, 0].min() - 1, X[:,0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:,1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                        np.arange(y_min, y_max, h))



    #tuned_parameters = [{'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}]
    #tuned_parameters = [{'kernel': ['poly'], 'C': [0.1, 1, 3], 'degree': [4,5,6],
    #                      'gamma': [0.1, 1]}]
    #tuned_parameters = [{'kernel': ['rbf'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100],
    #                     'gamma': [0.1, 0.5, 1, 3, 6, 10]}]

    grid = dict(max_depth=np.arange(1, 51),
                         min_samples_split=np.arange(2,11))
    print "here"
    #svr = svm.SVC()
    #clf = grid_search.GridSearchCV(svr, tuned_parameters, cv=5, scoring='accuracy')
    #clf = linear_model.LogisticRegressionCV(Cs=[0.1, 0.5, 1, 5, 10, 50, 100], cv=5,
    #                                        scoring='accuracy')
    #estimator = neighbors.KNeighborsClassifier()
    #estimator = tree.DecisionTreeClassifier()
    estimator = ensemble.RandomForestClassifier()
    clf = grid_search.GridSearchCV(estimator, param_grid=grid, cv=5, scoring='accuracy')
    print "here too"
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on training set:")
    print()
    print(clf.best_score_)

    plt.figure()

    # plot the contour for the prediction
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot the test points
    plt.scatter(X_test[:, 0], X_test[:, 1], marker='o', c=y_test)

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    # Get the score
    y_true, y_pred = y_test, clf.predict(X_test)
    print("Scores for the test data are:")
    print()
    print(clf.score(X_test, y=y_test))
    plt.show()


if __name__ == "__main__":
    main()
