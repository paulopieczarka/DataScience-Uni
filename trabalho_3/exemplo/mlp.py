"""
  uma rede neural MLP implementada segundo
  https://www.springboard.com/blog/beginners-guide-neural-network-in-python-scikit-learn-0-18/
  http://scikit-learn.org/stable/modules/cross_validation.html
  https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
"""

import pandas as pd
train = pd.read_csv('Copenhagen\\newA.csv', names = ["var1", "var2", "var3", "class"])

#>>> from sklearn.model_selection import train_test_split
#>>> X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)


#print train.head()
#print train.describe().transpose()
#print train.shape
xTrain = train.drop('class',axis=1)
yTrain = train['class']

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(activation='relu',hidden_layer_sizes=(8),max_iter=500)
print(mlp.fit(xTrain,yTrain))

#tests = mlp.predict(x)
#from sklearn.metrics import classification_report,confusion_matrix
#print(confusion_matrix(y,tests))
#print(classification_report(y,tests))


prediction = pd.read_csv('Copenhagen\\newB.csv', names = ["var1", "var2", "var3", "class"])
from sklearn.metrics import classification_report,confusion_matrix
xTest = prediction.drop('class',axis=1)
yTest = prediction['class']

tests = mlp.predict(xTest)
print(confusion_matrix(yTest,tests))
print(classification_report(yTest,tests))

from matplotlib import pyplot as plt
plt.scatter(yTest, tests)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()
