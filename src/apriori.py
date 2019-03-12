import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from scipy import io
from scipy import sparse

file_mat_ds = io.loadmat('dataset.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])
items = file_mat_ds['items']
max_ones = int(file_mat_ds['max_ones'])

print("Initialization...\n")
records = [['nan' for x in range(max_ones)] for y in range(7500)]
temp = []
tot = sparse.find(dataset)
k = 0

for i in range(0, len(tot[0])):

    if k == 20:
        k = 0
    records[tot[0][i]][k] = str(items[tot[1][i]])
    k += 1

#print(records)
print("Doing association...\n")
association_rules = apriori(records, min_support=0.006, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)

for item in association_results:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0]
    items = [x for x in pair]

    rule = "Rule:"
    for obj in items:
        rule = " " + rule + " --> " + obj
    print(rule)

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")

