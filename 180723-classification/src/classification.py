import sys
import statistics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def transform(A, means, deviations):
    for i in range(len(means)):
        A[:,i] = (A[:,i]-means[i])/deviations[i]
    return A

rand1 = 1#np.random.randint(100)
rand2 = 93#np.random.randint(100)
print(rand1, rand2)

df = pd.read_csv('./Input/training-s059.csv', header=None)
Y_train = df[0]
data = df.drop([0], axis=1)
X_train = data.to_numpy()

df = pd.read_csv(sys.argv[1], header=None)
Y_test = df[0]
data = df.drop([0], axis=1)
X_test = data.to_numpy()

means = []
deviations = []
for i in range(10):
    means.append(statistics.mean(X_train[:,i]))
    deviations.append(statistics.stdev(X_train[:,i]))

X_train = transform(X_train, means, deviations)
oversample = SMOTE(k_neighbors=4)
X_train_over, Y_train_over = oversample.fit_resample(X_train, Y_train)

forest = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=rand2, n_jobs=-1)
logistic = LogisticRegression(multi_class='multinomial', max_iter=200)
xgboost = XGBClassifier(random_state=rand2)
model = VotingClassifier(estimators=[('lr', forest), ('rf', logistic), ('gnb', xgboost)], voting='soft')
model.fit(X_train_over, Y_train_over)
# print('Training ->')
# Y_pred = model.predict(X_train_over)
# print(classification_report(Y_train_over, Y_pred))
# print(confusion_matrix(Y_train_over, Y_pred))
# print('Testing ->')
Y_pred = model.predict(transform(X_test, means, deviations))
print(classification_report(Y_test, Y_pred))
print(confusion_matrix(Y_test, Y_pred))
df = pd.DataFrame(Y_pred)
df.to_csv('./Output/answer-s059.csv', header=None, index=None)

# df = pd.read_csv('/content/drive/MyDrive/training-s059.csv', header=None)
# Y = df[0]
# data = df.drop([0], axis=1)
# X = data.to_numpy()

# sss = StratifiedShuffleSplit(n_splits=1, test_size=0.25, random_state=rand1)
# sss.get_n_splits(X, Y)
# for train_index, test_index in sss.split(X, Y):
#     X_train, X_test = X[train_index], X[test_index]
#     Y_train, Y_test = Y[train_index].to_list(), Y[test_index].to_list()
    
# means = []
# deviations = []
# for i in range(10):
#     means.append(statistics.mean(X_train[:,i]))
#     deviations.append(statistics.stdev(X_train[:,i]))

# X_train = transform(X_train, means, deviations)
# oversample = SMOTE(k_neighbors=3)
# X_train_over, Y_train_over = oversample.fit_resample(X_train, Y_train)

# forest = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=rand2, n_jobs=-1)
# logistic = LogisticRegression(multi_class='multinomial', max_iter=200)
# xgboost = XGBClassifier(random_state=rand2)
# model = VotingClassifier(estimators=[('lr', forest), ('rf', logistic), ('gnb', xgboost)], voting='soft')
# model.fit(X_train_over, Y_train_over)
# print('Training ->')
# Y_pred = model.predict(X_train_over)
# print(classification_report(Y_train_over, Y_pred))
# print(confusion_matrix(Y_train_over, Y_pred))
# print('Testing ->')
# Y_pred = model.predict(transform(X_test, means, deviations))
# print(classification_report(Y_test, Y_pred))
# print(confusion_matrix(Y_test, Y_pred))