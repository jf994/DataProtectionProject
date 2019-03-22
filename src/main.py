from scipy import io
import numpy as np
from scipy import sparse
import time

from get_privacy import calculate_privacy
from singleton import estimate_singleton
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

# threshold 0.25 come nel paper
threshold = 0.25
# set dell' n itemset
n = 1
# preparo il contenitore per le relazioni finali
relations = []

# calcolo privacy
calculate_privacy(support, p)

# Stima n-itemset support più colonne
t = time.time()

# calcolo M per l'n desiderato
M = calc_M(n, p)

print("\nM:\n{}".format(M))

# stima per il 2-itemset
if n == 1:
    # Stima singleton supports 1 colonna
    estimate_singleton(distorted, p, num_clients, M)
elif n == 2:
    estimate_2_itemset(dataset, distorted, n, M, threshold, items, relations)
# stima per il 3-itemset
elif n == 3:
    estimate_3_itemset(dataset, distorted, n, M, threshold, items, relations)

elapsed = time.time() - t
elapsed /= 3600

print("\ntime: {} ore".format(elapsed))
