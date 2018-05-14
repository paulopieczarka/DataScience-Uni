from __future__ import division
from linear_algebra import squared_distance, vector_mean, distance
import math, random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import operator
from numba import jit

# Remove not needed fields.
def clear_database(inputCSV, outputCSV):
  data = pd.read_csv(inputCSV, names = [
    "clearance_date",
    "clearance_status",
    "council_district_code",
    "description",
    "district",
    "latitude",
    "longitude",
    "timestamp",
    "clearance_days"
  ])

  data = data.drop(["clearance_date", "timestamp"], axis=1)
  data.to_csv(outputCSV, index=False, encoding='utf-8')

# Split the data into training and test data.
@jit
def loadDataset(filename, split, trainingSet=[] , testSet=[]):
  dataset = pd.read_csv(filename)
  for index, row in dataset.iterrows():
    if random.random() < split:
      trainingSet.append(row)
    else:
      testSet.append(row)

class KMeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k          # number of clusters
        self.means = None   # means of clusters
        
    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))
                   
    def train(self, inputs):
    
        self.means = random.sample(inputs, self.k)
        assignments = None
        
        while True:
            # Find new assignments
            new_assignments = map(self.classify, inputs)

            # If no assignments have changed, we're done.
            if assignments == new_assignments:                
                return

            # Otherwise keep the new assignments,
            assignments = new_assignments    

            for i in range(self.k):
                i_points = [p for p, a in zip(inputs, assignments) if a == i]
                # avoid divide-by-zero if i_points is empty
                if i_points:                                
                    self.means[i] = vector_mean(i_points)    

					
def squared_clustering_errors(inputs, k):
    """finds the total squared error from k-means clustering the inputs"""
    clusterer = KMeans(k)
    clusterer.train(inputs)
    means = clusterer.means
    assignments = map(clusterer.classify, inputs)
    
    return sum(squared_distance(input,means[cluster])
               for input, cluster in zip(inputs, assignments))


if __name__ == "__main__":

    filename = 'base/result_min.csv'

    # trainingSet=[]
    # testSet=[]
    # split = 0.67
    # loadDataset('base/result_min.csv', split, trainingSet, testSet)

    # print('Train set: ' + repr(len(trainingSet)))
    # print('Test set: ' + repr(len(testSet)))

    dataset = pd.read_csv(filename)

    col1 = 'district'
    col2 = 'clearance_days'

    inputs = dataset[[col1, col2]]
    # inputs = inputs[:-1]

    coords = inputs.as_matrix(columns=None)

    # series1 = inputs.iloc[0,:]
    print(coords[0:1])

    # print([[0,1],[-1,2]])
    # print(inputs[0:1])

    inputs = np.array(coords)

    x = [row[0] for row in inputs]
    y = [row[1] for row in inputs]
    plt.scatter(x, y)
    plt.title("teste")
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.show()