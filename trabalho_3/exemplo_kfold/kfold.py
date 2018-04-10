"""
  uma rede neural MLP implementada segundo
  https://www.springboard.com/blog/beginners-guide-neural-network-in-python-scikit-learn-0-18/
  http://scikit-learn.org/stable/modules/cross_validation.html
  https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
"""
from sklearn.model_selection import KFold 
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report, confusion_matrix

import pandas as pd
import numpy as np
import pickle
data = pd.read_csv('..\\data\\Copenhagen\\newA.csv', names = ["var1", "var2", "var3", "class"])


functions = ['identity', 'logistic', 'tanh', 'relu']
neurons = [5, 6, 7, 8, 9, 10]
iterations = [800, 900, 1000, 1100, 1200]

subconjuntos = 10
kf = KFold(n_splits=subconjuntos)  
kf.get_n_splits(data)
melhorFuncao = ''
maiorMediaAcerto = 0
neuron = 0
it = 0
rede = MLPClassifier()
for i in iterations:
	for n in neurons:
		for f in functions:
			mediaAcerto = 0
			for train, test in kf.split(data):  
				IN = np.array(data.drop('class',axis=1))
				OUT = np.array(data['class'])
				X_train, X_test, Y_train, Y_test = IN[train], IN[test], OUT[train], OUT[test]
				mlp = MLPClassifier(activation=f, hidden_layer_sizes=(n), max_iter=i)
				mlp.fit(X_train,Y_train)
				classes = mlp.predict(X_test)
				mediaAcerto = precision_score(Y_test, classes, average="macro") + mediaAcerto
				#print precision_score(Y_test, classes, average="macro")
				#print(confusion_matrix(Y_test,classes))
				#print(classification_report(Y_test,classes))
			
			mediaAcerto = mediaAcerto / subconjuntos
			print(f, n, i, mediaAcerto)
			if (mediaAcerto > maiorMediaAcerto):
				melhorFuncao = f
				neuron = n
				it = i
				maiorMediaAcerto = mediaAcerto
				rede = mlp
				# save the model to disk
				filename = '..\\data\\Copenhagen\\rede.sav'
				pickle.dump(rede, open(filename, 'wb'))

print (melhorFuncao, neuron, it, maiorMediaAcerto)


rede = pickle.load(open('..\\data\\Copenhagen\\rede.sav', 'rb'))
prediction = pd.read_csv('..\\data\\Copenhagen\\newB.csv', names = ["var1", "var2", "var3", "class"])

xTest = prediction.drop('class',axis=1)
yTest = prediction['class']
tests = rede.predict(xTest)
print(confusion_matrix(yTest,tests))
print(classification_report(yTest,tests))

from matplotlib import pyplot as plt
plt.scatter(yTest, tests)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()
	