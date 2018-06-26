import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as pl
from matplotlib.colors import ListedColormap
from sklearn import preprocessing, neighbors

from psutil import virtual_memory
mem = virtual_memory()
print(mem)

def load_dataset(dataset_path):
  data = pd.read_csv(dataset_path, names = [
    "FID",
    "UF",
    "Municipio",
    "Faixa_de_r",
    "Produto",
    "Valor",
    "Concluidas",
    "Entregues",
    "Percentual",
    "IF",
    "Latitude",
    "Longitude"
  ])
  
  data = data.drop(["FID"], axis=1)
  data_array = data.as_matrix(columns=None)
  data_array = np.delete(data_array, (0), axis=0)
  return data_array

def label_dataset(data):
  col = []
  col.append(np.squeeze(np.asarray(data[:, 6])))
  col.append(np.squeeze(np.asarray(data[:, 7])))
  col.append(np.squeeze(np.asarray(data[:, 0])))
  
  for i in range(0, 3):
    column = np.squeeze(np.asarray(col[i]))
    le = preprocessing.LabelEncoder()
    col[i] = le.fit_transform(column)

  return np.column_stack((col[0], col[1], col[2]))

def classify_and_fit(data):
  X = np.column_stack((data[:, 0], data[:, 1]))
  y = data[:, 2]

  n_neighbors = 15

  h = .02 # step size in the mesh

  cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF', '#FFAAFF', '#AAFFFF'])
  cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF', '#FF00FF', '#00FFFF'])

  for weights in ['distance']:
      # we create an instance of Neighbours Classifier and fit the data.
      clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
      clf.fit(X, y)

      # Plot the decision boundary. For that, we will assign a color to each
      # point in the mesh [x_min, x_max]x[y_min, y_max].
      x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
      y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
      xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                          np.arange(y_min, y_max, h))
      Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

      # Put the result into a color plot
      Z = Z.reshape(xx.shape)
      pl.figure()
      pl.pcolormesh(xx, yy, Z, cmap=cmap_light)

      # Plot also the training points
      pl.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                  edgecolor='k', s=20)
      pl.xlim(xx.min(), xx.max())
      pl.ylim(yy.min(), yy.max())
      pl.title("3-Class classification (k = %i, weights = '%s')"
                % (n_neighbors, weights))

  pl.show()


def main():
  dataset_path = './casa.csv'
  data = load_dataset(dataset_path)

  data = label_dataset(data)
  # data = preprocessing.normalize(data)
  classify_and_fit(data)

  # pl.scatter(data[:, 0], data[:, 1])
  # # pl.xticks(ks)
  # pl.xlabel("k")
  # pl.ylabel("total squared error")
  # pl.show()

  

main()
