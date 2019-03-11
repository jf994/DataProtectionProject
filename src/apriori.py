import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from scipy import io
from scipy import sparse

file_mat_ds = io.loadmat('dataset_500.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])

records = []
for i in range(0, 500):
    records.append([str(dataset.A[i,j]) for j in range(0, 200)])

print('ciao\n')
association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)

print(association_rules[0])