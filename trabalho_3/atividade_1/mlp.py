"""
  uma rede neural MLP implementada segundo
  https://www.springboard.com/blog/beginners-guide-neural-network-in-python-scikit-learn-0-18/
  http://scikit-learn.org/stable/modules/cross_validation.html
  https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
"""

import pandas as pd
import numpy as np
from sklearn.metrics import precision_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

funcs = ['identity', 'logistic', 'tanh', 'relu']

train = pd.read_csv('Edinburgo\\A3.csv', names = ["var1", "var2", "var3", "class"])
xTrain = train.drop('class',axis=1)
yTrain = train['class']

prediction = pd.read_csv('Edinburgo\\B3.csv', names = ["var1", "var2", "var3", "class"])
xTest = prediction.drop('class',axis=1)
yTest = prediction['class']

bestPrecision = 0
bestNetwork = MLPClassifier()

for f in funcs:
  for numLayers in range(5, 10):
    for numIt in range(800, 1200, 100):

      mlp = MLPClassifier(activation=f, hidden_layer_sizes=(numLayers), max_iter=numIt)
      mlp.fit(xTrain, yTrain)

      tests = mlp.predict(xTrain)
      newPrecision = precision_score(yTrain, tests, average='macro')

      if newPrecision > bestPrecision:
        print("Precision score: {}".format(newPrecision))
        print(f, numLayers, numIt)
        print("~~~~>")
        bestPrecision = newPrecision
        bestNetwork = mlp

print(bestPrecision)

tests = bestNetwork.predict(xTest)
newPrecision = precision_score(yTest,tests, average='macro')
print(newPrecision)

from matplotlib import pyplot as plt
plt.scatter(yTest, tests)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()
