import numpy as np
import pandas as pd
from collections import Counter

data = pd.read_csv("KWData.dat", sep=';')
data.sum(axis=0)
data.sum(axis=1)

trsld = 0.0001

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


#OC Dataset
file.seek(0)
OCset = set()
OCdict = {}

for row in file:
    if(row[0:2] in ('OC')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "OC"):
            for word in words:
                OCset.add(word.lstrip())

OCMatrix = np.zeros((len(IDset),len(OCset)), dtype='uint8')
OCDataFrame = pd.DataFrame(data=OCMatrix, index=IDset, columns=OCset)

file.seek(0)
for row in file:
    if(row[0:2] in ('ID','OC')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            idname = words[0].lstrip()
        if(line[0] == "OC"):
            for word in words:
                ocname = word.lstrip()
                OCDataFrame[ocname][idname] = 1

OCDataFrame.to_csv("OCData.dat", sep=';')

##--
#KW Dataset
file.seek(0)
KWset = set()

for row in file:
    if(row[0:2] in ('KW')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "KW"):
            for word in words:
                KWset.add(word.lstrip())

KWMatrix = np.zeros((len(IDset),len(KWset)), dtype='uint8')
KWDataFrame = pd.DataFrame(data=KWMatrix, index=IDset, columns=KWset)

file.seek(0)
for row in file:
    if(row[0:2] in ('ID','KW')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            idname = words[0].lstrip()
        if(line[0] == "KW"):
            for word in words:
                kwname = word.lstrip()
                KWDataFrame[kwname][idname] = 1

KWDataFrame.to_csv("KWData.dat", sep=';')

##--
#DR Embl Dataset
file.seek(0)
DREMBLdict = {}
DREMBLset = set()

for row in file:
    if(row[0:2] in ('DR')):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "DR"):
            if(words[0] == "EMBL"):
                keyDR = words[1].lstrip();
                if( keyDR in DREMBLdict):
                    DREMBLdict[keyDR] = DREMBLdict[keyDR]+1
                else:
                    DREMBLdict[keyDR] = 1
nTot = len(DREMBLdict)
for DRkey in DREMBLdict:
    if (DREMBLdict[DRkey]/nTot >= trsld):
        DREMBLset.add(DRkey)

DREMBLMatrix = np.zeros((len(IDset),len(DREMBLset)), dtype='uint8')
DREMBLDataFrame = pd.DataFrame(data=DREMBLMatrix, index=IDset, columns=DREMBLset)

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
            if(words[0] == "EMBL"):
                if (words[1] in DREMBLset):
                    DRstring = words[1].lstrip()
                    DREMBLDataFrame[DRstring][idname] = 1

DREMBLDataFrame.to_csv("DREMBLData.dat", sep=';')
