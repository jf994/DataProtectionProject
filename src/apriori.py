import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from scipy import io
from scipy import sparse

# carico i dati presenti sul file .mat
file_mat_ds = io.loadmat('dataset.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])
items = file_mat_ds['items']
max_ones = int(file_mat_ds['max_ones'])

# inizializzazione matrice records che passerò alla funzione apriori
print("Initialization...\n")
records = [['nan' for x in range(max_ones)] for y in range(7500)]
temp = []
# salvo in tot le posizioni (riga, colonna) dei valori diversi da zero presenti in dataset, ed il loro valore (sempre 1)
tot = sparse.find(dataset)
k = 0

# costrusco la matrice records secondo il formato atteso dalla funzione apriori
for i in range(0, len(tot[0])):

    if k == 20:
        k = 0
    records[tot[0][i]][k] = str(items[tot[1][i]])
    k += 1

# chiamo la funzione apriori settando opportuni parametri
print("Doing association...\n")
association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)

# stampo i risultati ottenuti
for item in association_results:

    pair = item[0]
    items = [x for x in pair]

    rule = "Rule:"
    if len(items) == 2:
        for obj in items:
            rule = " " + rule + " --> " + obj
        print(rule)

        #second index of the inner list
        print("Support: " + str(item[1]))

        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")

