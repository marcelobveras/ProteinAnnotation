import numpy as np
import pandas as pd
from sklearn import tree
from sklearn import model_selection as  ms
from sklearn import metrics as mt
import graphviz
from  anytree import Node, RenderTree

dataX = pd.read_csv("Data.dat",sep=';')
dataY = pd.read_csv("KWData.dat", sep=';')

X_train, X_test, y_train, y_test = ms.train_test_split(dataX.values[:,1:].astype(bool),
 dataY.values[:,1:].astype(bool), test_size=0.33, random_state=42)
[n, m] = X_train.shape
[m2, n2] = y_train.shape

# y_train1 = y_train[:,0]
#
# nivelMax = 5
#
# class DecisionNode:
#     def __init__(self, val):
#         self.l = None
#         self.r = None
#         self.v = val
#     rule = None
#     gini = 0
#
# Root = DecisionNode(X_train)
#
#
# def c45(Dataroot):
#     somaTrue = sum(X_test)
#     somaFalse = sum(~X_test)
#     probTrue = somaTrue/n
#     probFalse = somaFalse/n
#     probLogTrue = np.log2(probTrue)
#     probLogFalse = np.log2(probFalse)
#     EntropyTrue = -somaTrue*probTrue*probLogTrue
#     EntropyFalse = -somaFalse*probFalse*probLogFalse
#     Entropy = EntropyTrue+EntropyFalse
#     idxMaxEnt = Entropy.argmax()
#

clf = tree.DecisionTreeClassifier(max_depth=4)
clf = clf.fit(X_train,y_train)
y_hat = clf.predict(X_test)
y_hat.shape[0]

TP = np.zeros([y_hat.shape[1]])
FP = np.zeros([y_hat.shape[1]])
TN = np.zeros([y_hat.shape[1]])
FN = np.zeros([y_hat.shape[1]])

for i in range(y_hat.shape[0]):
    for j in range(y_hat.shape[1]):
        if y_test[i,j]==y_hat[i,j]==1:
           TP[j] += 1
        if y_hat[i,j]==1 and y_test[i,j]!=y_hat[i,j]:
           FP[j] += 1
        if y_test[i,j]==y_hat[i,j]==0:
           TN[j] += 1
        if y_hat[i,j]==0 and y_test[i,j]!=y_hat[i,j]:
           FN[j] += 1
z = 1.96
n = TP + FP
np.seterr(divide='ignore', invalid='ignore')

p = np.divide(TP,n)

conf = np.zeros([y_hat.shape[1]])
conf[:] = np.nan
for j in range(y_hat.shape[1]):
    if (~np.isnan(p[j])):
        conf[j] = (p[j] + ((z*z)/(2*n[j])) - z * (np.sqrt( (p[j]/n[j]) - ((p[j]*p[j])/n[j]) + ((z*z)/(4*n[j]*n[j]))  )))/ (1+((z*z)/(n[j])))
p[np.where(conf < 0.5)] = np.nan
p[np.where(~np.isnan(p))]
conf[np.where(~np.isnan(p))]
# dataY[dataY.columns[1:][np.where(~np.isnan(p))]]
# dataY[dataY.columns[1:][~np.isnan(p)]]
dataY.columns[1:][np.where(~np.isnan(p))[0][0]]
y_test[:,np.where(p==1)] == y_hat[:,np.where(p==1)]



sum(TP)
sum(FP)
sum(TN)
sum(FN)
for Target, Predicted in zip(y_test.transpose(),y_hat.transpose()):
    prec = mt.precision_score(Target,Predicted)
    if (prec > 0):
        print(prec)

#dataY.sum(axis=0, numeric_only=True)
#p = dataX.sum(axis=0, numeric_only=True)/dataX.shape[0]
# a = np.array([[1,2],[3,4]])
# b = np.array([[5,6],[7,8]])
# for col1, col2 in zip(a.transpose(),b.transpose()):
#     print(col1)
#     print(col2)

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("Data")
