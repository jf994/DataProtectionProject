from scipy import io
import numpy as np
from scipy import sparse
import time

from get_privacy import calculate_privacy
from singleton import estimate_singleton, bad_estimate_singleton
from calculate_M import calc_M
from due_itemset import estimate_2_itemset
from tre_itemset import estimate_3_itemset

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

# calcolo privacy
calculate_privacy(support, p)

# Stima singleton supports 1 colonna
estimate_singleton(distorted, p, num_clients)

# Stima errata (metodo paper)
bad_estimate_singleton(distorted, p, num_clients)


# Stima n-itemset support più colonne
t = time.time()

relations = []
# threshold calcolato come circa 10% di 7500
threshold = 0.25
n = 2

M = calc_M(n, p)

print("\nM_big:\n{}".format(M))

# stima per il 2-itemset
if n == 2:
    estimate_2_itemset(dataset, distorted, n, M, threshold, items, relations)
# stima per il 3-itemset
elif n == 3:
    estimate_3_itemset(dataset, distorted, n, M, threshold, items, relations)

elapsed = time.time() - t
print("\ntime: {}".format(elapsed))
