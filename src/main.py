from scipy import io
import numpy as np
from scipy import sparse
import time
from itertools import combinations

from get_privacy import calculate_privacy
from enne_itemset import estimate_n_itemset

# Carico i valori salvati nei file .mat
file_mat_ds = io.loadmat('dataset.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])
items = file_mat_ds['items']
num_items = len(np.array(file_mat_ds['items']))
support = float(file_mat_ds['support'])

file_mat_dist = io.loadmat('distorted.mat')
distorted = np.matrix(file_mat_dist['distorted'])
p = float(file_mat_dist['p'])
num_clients = len(distorted[:, 1])

# threshold 0.0025 come nel paper
threshold = 0.025
print("\nthreshold: {}\n".format(threshold))

# preparo il contenitore per le relazioni finali
relations = []

# calcolo privacy
calculate_privacy(support, p)

# Stima n-itemset support più colonne
t = time.time()

comb = combinations(list(range(10, 25)), 1)

estimate_n_itemset(dataset, distorted, 1, p, threshold, items, relations, comb)

elapsed = time.time() - t
elapsed /= 3600

print("\ntime: {} ore".format(elapsed))
