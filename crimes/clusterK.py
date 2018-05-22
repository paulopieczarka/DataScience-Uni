from __future__ import division
from linear_algebra import squared_distance, vector_mean, distance
import math, random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import operator
import seaborn as sns
from numba import jit, vectorize, autojit, njit

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
        self.last_assignments = None

     
    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):
    
        self.means = random.sample(inputs, self.k)
        assignments = None
        
        its = 0
        print(self.k)
        while True:
            
            # Find new assignments
            new_assignments = list(map(self.classify, inputs))

            #print('KMeans.. ', its)
            #its += 1

            # If no assignments have changed, we're done.
            if assignments == new_assignments:    
                self.last_assignments = assignments            
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

@jit
def cuda_find_mah_errors(inputs, ks):
    arr = []
    for k in ks:
        arr.append(squared_clustering_errors(list(inputs), k))
    return arr

if __name__ == "__main__":

    filename = 'base/result_min.csv'

    # trainingSet=[]
    # testSet=[]
    # split = 0.67
    # loadDataset('base/result_min.csv', split, trainingSet, testSet)

    # print('Train set: ' + repr(len(trainingSet)))
    # print('Test set: ' + repr(len(testSet)))

    dataset = pd.read_csv(filename)

    # TEST 1 description, clearance_days
    # TEST 2 council_district_code, clearance_days
    # TEST 3 district, description
    # TEST 4 description, clearance_days
    # TEST 5 council_district_code, clearance_status
    col1 = 'description'
    col2 = 'clearance_days'

    inputs = dataset[[col1, col2]]
    # inputs = inputs[:-1]

    coords = inputs.as_matrix(columns=None)

    # series1 = inputs.iloc[0,:]
    # print(coords[0:1])

    # print([[0,1],[-1,2]])
    # print(inputs[0:1])

    #inputs = np.array(coords)
    inputs = np.array(coords)
    ti = inputs.transpose()
    # print (inputs)
    # print (len(inputs))

    crimes = ['THEFT','THEFT BY SHOPLIFTING','BURGLARY OF RESIDENCE','THEFT OF LICENSE PLATE','BURGLARY NON RESIDENCE','BURGLARY OF VEHICLE','AGG ASLT STRANGLE/SUFFOCATE','AGG ASSAULT','THEFT OF VEHICLE/OTHER','AUTO THEFT','AGG ASSAULT FAM/DATE VIOLENCE','THEFT FROM AUTO','RAPE','BURGLARY OF COIN-OP MACHINE','THEFT OF BICYCLE','AGG ROBBERY/DEADLY WEAPON','AGG ASSAULT WITH MOTOR VEH','BREACH OF COMPUTER SECURITY','RAPE OF A CHILD','THEFT FROM BUILDING','THEFT FROM PERSON','BURG NON RESIDENCE SHEDS','AGG RAPE OF A CHILD','THEFT CATALYTIC CONVERTER','ROBBERY BY THREAT','THEFT OF AUTO PARTS','CAPITAL MURDER','MURDER','ROBBERY BY ASSAULT','DEADLY CONDUCT','THEFT OF METAL','AGG ASLT W/MOTOR VEH FAM/DAT V','AGG ASLT ENHANC STRANGL/SUFFOC','TAKE WEAPON FRM POLICE OFFICER','MISAPPLY FIDUCIARY PROP','AGG RAPE','AGG ROBBERY BY ASSAULT','PURSE SNATCHING','AGG ASSAULT ON PUBLIC SERVANT','AIRPORT - BREACH OF SECURITY','BURG OF RES - SEXUAL NATURE','DEADLY CONDUCT FAM/DATE VIOL','THEFT OF HEAVY EQUIPMENT','THEFT/TILL TAPPING','MANSLAUGHTER']    
    
    t2 = []
    for c in ti[0]:
        c0 = int(c/6)
        t2.append(crimes[c0])
    
    df = pd.DataFrame(dict(crime=ti[0], dias_para_completar=ti[1], color=t2, crimes=ti[0]))

    sns.lmplot('crime', 'dias_para_completar', data=df, hue='color', fit_reg=False)
    plt.title('Tempo para finalizar um crime')
    plt.show()



    # # Unique category labels: 'D', 'F', 'G', ...
    # color_labels = df['crimes'].unique()

    # # # List of RGB triplets
    # rgb_values = sns.color_palette("Set2", len(color_labels))

    # # # Map label to RGB
    # color_map = dict(zip(color_labels, rgb_values))

    # # # Finally use the mapped values
    # plt.scatter(df['c1'], df['c2'], c=df['color'].map(color_map))
    # plt.show()

    x = [row[0] for row in inputs]
    y = [row[1] for row in inputs]
    # plt.scatter(x, y)
    # plt.title(col1+" X "+col2)
    # plt.xlabel(col1)
    # plt.ylabel(col2)
    # plt.show()

    # ks = range(1, 12) # range(1, len(inputs) + 1)
    # errors = [squared_clustering_errors(list(inputs), k) for k in ks]
    # errors = cuda_find_mah_errors(list(inputs), ks)    
    # plt.plot(ks, errors)
    # plt.xticks(ks)
    # plt.xlabel("k")
    # plt.ylabel("total squared error")
    # plt.show()

    random.seed(0) # so you get the same results as me
    clusterer = KMeans(8)
    clusterer.train(list(inputs))
    print("3-means:")
    print(clusterer.means)
    print(clusterer.last_assignments)

    # plt.plot(x, y, 'o')
    plt.title("distribuicao pontos")
    # plt.xlabel(col1)
    # plt.ylabel(col2)
    df = pd.DataFrame(dict(crime=ti[0], dias_para_completar=ti[1], color=clusterer.last_assignments, crimes=ti[0]))
    sns.lmplot('crime', 'dias_para_completar', data=df, hue='color', fit_reg=False)
    clusterX = [row[0] for row in clusterer.means]
    clusterY = [row[1] for row in clusterer.means]
    plt.plot(clusterX, clusterY, 'rs')
    plt.show()
    