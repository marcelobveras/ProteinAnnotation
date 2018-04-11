import numpy as np
import pandas as pd

file = open("C:\\Users\\marce\\Desktop\\uniprot\\mammals.dat")

#Primeira Leitura
#Criação dos conjuntos de palavras

Codes = {'OC', 'DR', 'ID', 'KW'}
OCset = set()
DRset = set()
KWset = set()
IDset = set()

for row in file:
    #print(row[0:2])
    if(row[0:2] in Codes):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            IDset.add(words[0].lstrip())
        if(line[0] == "OC"):
            for word in words:
                OCset.add(word.lstrip())
        if(line[0] == "KW"):
            for word in words:
                KWset.add(word.lstrip())
        if(line[0] == "DR"):
            DRstring = words[0].lstrip()+':'+words[1].lstrip()
            DRset.add(DRstring)

#Incializando matrizes booleanas e dataframes correspondentes
OCMatrix = np.zeros((len(IDset),len(OCset)), dtype=int)
DRMatrix = np.zeros((len(IDset),len(DRset)), dtype=int)
KWMatrix = np.zeros((len(IDset),len(KWset)), dtype=int)

OCDataFrame = pd.DataFrame(data=OCMatrix, index=IDset, columns=OCset)
DRDataFrame = pd.DataFrame(data=DRMatrix, index=IDset, columns=DRset)
KWDataFrame = pd.DataFrame(data=KWMatrix, index=IDset, columns=KWset)


#Segunda leitura do arquivo (Criação do dataset)
file.seek(0)
for row in file:
    if(row[0:2] in Codes):
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
        if(line[0] == "KW"):
            for word in words:
                kwname = word.lstrip()
                KWDataFrame[kwname][idname] = 1
        if(line[0] == "DR"):
            DRstring = words[0].lstrip()+':'+words[1].lstrip()
            DRDataFrame[DRstring][idname] = 1
DRDataFrame.to_csv("DRdata", sep=';')
OCDataFrame.to_csv("OCData", sep=';')
KWDataFrame.to_csv("KWData", sep=';')
