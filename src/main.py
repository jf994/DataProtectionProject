from scipy import io
import numpy as np
from scipy import sparse

# Carico i valori salvati nei file .mat
file_mat_ds = io.loadmat('dataset_5000.mat')
dataset = sparse.csr_matrix(file_mat_ds['dataset'])
items = int(file_mat_ds['items'])
support = float(file_mat_ds['support'])


file_mat_dist = io.loadmat('distorted_5000.mat')
distorted = np.matrix(file_mat_dist['distorted'])
p = float(file_mat_dist['p'])
num_clients = len(distorted[:, 1])

# calcolo R1(p), R0(p), R per calcolare poi la privacy ottenuta

R1 = ((support * pow(p, 2)) / (support * p + (1 - support) * (1 - p))) \
    + ((support * pow(1 - p, 2)) / (support * (1 - p) + (1 - support) * p))

R0 = (((1 - support) * pow(p, 2)) / ((1 - support) * p + support * (1 - p))) \
    + (((1 - support) * pow(1 - p, 2)) / (support * p + (1 - support) * (1 - p)))

a = .9

R = a * R1 + (1 - a) * R0

privacy = (1 - R) * 100

print("User Privacy raggiunta: {}%".format(privacy))

# Stima singleton supports colonna 1

j = 2

# conto gli uni
C1_D = int(sum(distorted[:, j] == 1))

# conto gli zeri
C0_D = num_clients - C1_D

# DA METTERE APPOSTO
M = np.matrix([[p, 1-p], [1-p, p]])

C_D = np.matrix([[C1_D], [C0_D]])
print(C_D)
C_T = np.dot(np.linalg.inv(M), C_D)
print(C_T)
