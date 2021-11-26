import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn.ensemble import IsolationForest

df = pd.read_csv('./Input/anomaly-s059.dat', sep='\t', header=None).dropna(axis=1)

Output = []
for i in range(100):
    Y = df[i].tolist()
    Y = np.array(Y).reshape(-1,1)
    # model = DBSCAN(eps = 1.35, min_samples=10)
    # out = model.fit_predict(Y)
    
    clf = LocalOutlierFactor(n_neighbors=12, contamination=0.048)
    out = clf.fit_predict(Y)
    Output.append(out)
    l = [i for i in range(len(out)) if out[i]==-1]
    # print(l)

Output = np.array(Output).T
# count=0
# for i in range(100):
#     for j in range(100):
#         if Output[i][j]==-1:
#             count = count+1
# print(count)

df = pd.DataFrame(Output)
df.to_csv('./answer-s059.csv', sep='\t', header=None, index=None)