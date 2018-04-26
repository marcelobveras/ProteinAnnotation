import numpy as np
import pandas as pd
from collections import Counter

OCtresh = 0.05
DRtresh = 0.001
Codes = {'OC', 'DR', 'KW'}

file = open("C:\\Users\\marce\\Desktop\\uniprot\\mammals.dat")

#ID Set
IDset = set()
for row in file:
    if(row[0:2] == ('ID')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            IDset.add(words[0].lstrip())


# #OC Dataset
# file.seek(0)
# OCset = set()
#
# for row in file:
#     if(row[0:2] in ('OC')):
#         line = row.split("   ")
#         line[-1] = line[-1].strip()
#         line = [empEle for empEle in line if empEle]
#         line[-1] =  line[-1][:-1]
#         words = line[1].split(';')
#         if(line[0] == "OC"):
#             for word in words:
#                 OCset.add(word.lstrip())
#
# OCMatrix = np.zeros((len(IDset),len(OCset)), dtype='uint8')
# OCDataFrame = pd.DataFrame(data=OCMatrix, index=IDset, columns=OCset)
#
# file.seek(0)
# for row in file:
#     if(row[0:2] in ('ID','OC')):
#         line = row.split("   ")
#         line[-1] = line[-1].strip()
#         line = [empEle for empEle in line if empEle]
#         line[-1] =  line[-1][:-1]
#         words = line[1].split(';')
#         if(line[0] == "ID"):
#             idname = words[0].lstrip()
#         if(line[0] == "OC"):
#             for word in words:
#                 ocname = word.lstrip()
#                 OCDataFrame[ocname][idname] = 1
#
# OCDataFrame.to_csv("OCData.dat", sep=';')
#
# ##--
# #KW Dataset
# file.seek(0)
# KWset = set()
#
# for row in file:
#     if(row[0:2] in ('KW')):
#         line = row.split("   ")
#         line[-1] = line[-1].strip()
#         line = [empEle for empEle in line if empEle]
#         line[-1] =  line[-1][:-1]
#         words = line[1].split(';')
#         if(line[0] == "KW"):
#             for word in words:
#                 KWset.add(word.lstrip())
#
# KWMatrix = np.zeros((len(IDset),len(KWset)), dtype='uint8')
# KWDataFrame = pd.DataFrame(data=KWMatrix, index=IDset, columns=KWset)
#
# file.seek(0)
# for row in file:
#     if(row[0:2] in ('ID','KW')):
#         line = row.split("   ")
#         line[-1] = line[-1].strip()
#         line = [empEle for empEle in line if empEle]
#         line[-1] =  line[-1][:-1]
#         words = line[1].split(';')
#         if(line[0] == "ID"):
#             idname = words[0].lstrip()
#         if(line[0] == "KW"):
#             for word in words:
#                 kwname = word.lstrip()
#                 KWDataFrame[kwname][idname] = 1
#
# KWDataFrame.to_csv("KWData.dat", sep=';')

##--
#DR Embl Dataset
file.seek(0)
DRdict = {}
DRset = set()
OCset = set()
OCdict = {}

for row in file:
    if(row[0:2] in ('DR','OC')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "DR"):
            #if(words[0] == "EMBL"):
            keyDR = 'DR:'+words[0]+':'+words[1].lstrip();
            if( keyDR in DRdict):
                DRdict[keyDR] = DRdict[keyDR]+1
            else:
                DRdict[keyDR] = 1
        if(line[0] == "OC"):
            for word in words:
                keyOC = 'OC:'+word.lstrip();
                if( keyOC in OCdict):
                    OCdict[keyOC] = OCdict[keyOC]+1
                else:
                    OCdict[keyOC] = 1

nTotDR = len(DRdict)
nTotOC = len(OCdict)

for OCkey in OCdict:
    if (OCdict[OCkey]/nTotOC >= OCtresh):
        OCset.add(OCkey)
# len(OCset)
for DRkey in DRdict:
    if (DRdict[DRkey]/nTotDR >= DRtresh):
        DRset.add(DRkey)
# len(DRset)
len(OCset.union(DRset))
featMatrix = np.zeros((len(IDset),len(DRset)+len(OCset)), dtype='uint8')
featDataFrame = pd.DataFrame(data=featMatrix, index=IDset, columns=OCset.union(DRset))

file.seek(0)
for row in file:
    if(row[0:2] in ('ID','DR')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            idname = words[0].lstrip()
        if(line[0] == "DR"):
            #if(words[0] == "EMBL"):
            DRstring = 'DR:'+words[0]+':'+words[1].lstrip()
            if (DRstring in DRset):
                featDataFrame[DRstring][idname] = 1
        if(line[0] == "OC"):
            for word in words:
                ocname = 'OC:'+word.lstrip()
                featDataFrame[ocname][idname] = 1
featDataFrame.sum()
DRDataFrame.to_csv("Data.dat", sep=';')
