import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from scipy import io
from scipy import sparse

file_mat_ds = io.loadmat('../docs/dataset.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])
items = file_mat_ds['items']

print("Initialization...\n")
records = [["nan" for x in range(120)] for y in range(7500)]
temp = []
tot = sparse.find(dataset)

for i in range(0, len(tot[0])):
    print(str(i)+"\n")
    records[tot[0][i]][tot[1][i]] = str(items[tot[1][i]])

print(records)
print("Doing association...\n")
association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)

print(association_results[0])
