from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def get_columns(db, col1, col2):
  inputs = db[[col1, col2]]
  coords = inputs.as_matrix(columns=None)
  return np.array(coords)

def plot_colored_graph(inputs, kmeans_result):
  x = inputs.transpose()

  df = pd.DataFrame(dict(
    crime=x[0],
    dias_para_completar=x[1],
    color=x[0]
  ))

  sns.lmplot('crime', 'dias_para_completar', data=df, hue='color', fit_reg=False)
  plt.title('Tempo para finalizar um crime')

  clusterX = [row[0] for row in kmeans_result]
  clusterY = [row[1] for row in kmeans_result]
  plt.plot(clusterX, clusterY, 'rs')

  plt.show()

def find_elbow(inputs, max_k):
  distorsions = []
  for k in max_k:
      kmeans = KMeans(n_clusters=k)
      kmeans.fit(inputs)
      distorsions.append(kmeans.inertia_)

  plt.plot(max_k, distorsions)
  plt.title('Elbow curve')

def main():
  # Load dataset
  crimes_db = pd.read_csv('base/result_min.csv')
  inputs = get_columns(crimes_db, 'description', 'clearance_days')

  # find best k
  find_elbow(inputs, range(2, 20))

  # run k-means
  kmeans = KMeans(n_clusters=8, random_state=0).fit(inputs)
  print(kmeans.cluster_centers_)

  plot_colored_graph(inputs, kmeans.cluster_centers_)

main()
