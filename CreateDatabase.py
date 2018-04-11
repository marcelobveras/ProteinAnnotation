import numpy as np

file = open("C:\\Users\\marce\\Desktop\\uniprot\\mammals001.dat")


#Primeira Leitura
#Criação dos conjuntos de palavras

Codes = {'OC', 'DR', 'ID', 'KW'}
OCset = set()
DRset = set()
KWset = set()
idCount = 0

for row in file:
    #print(row[0:2])
    if(row[0:2] in Codes):
        line = row.split("   ")
        line[-1] = line[-1].strip()
        line = [empEle for empEle in line if empEle]
        line[-1] =  line[-1][:-1]
        words = line[1].split(';')
        if(line[0] == "ID"):
            idCount = idCount+1
        if(line[0] == "OC"):
            for word in words:
                OCset.add(word.lstrip())
        if(line[0] == "KW"):
            for word in words:
                KWset.add(word.lstrip())
        if(line[0] == "DR"):
            DRstring = words[0].lstrip()+':'+words[1].lstrip()
            DRset.add(DRstring)

#Creando matrizes booleanas
OCMatrix = np.zeros((idCount,len(OCset)), dtype=bool);
DRMatrix = np.zeros((idCount,len(KWset)), dtype=bool);
KWMatrix = np.zeros((idCount,len(DRset)), dtype=bool);
