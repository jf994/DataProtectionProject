from scipy import io
import numpy as np

# Carico i valori salvati nei file .mat
file_mat_ds = io.loadmat('dataset_5000.mat')
dataset = file_mat_ds['dataset']
items = file_mat_ds['items']
support = file_mat_ds['support']

file_mat_dist = io.loadmat('distorted_5000.mat')
distorted = file_mat_dist['distorted']
p = file_mat_dist['p']
num_clients = len(distorted[:, 1])

# calcolo R1(p), R0(p), R per calcolare poi la privacy ottenuta

R1 = ((support * pow(p, 2)) / (support * p + (1 - support) * (1 - p))) \
    + ((support * pow(1 - p, 2)) / (support * (1 - p) + (1 - support) * p))

R0 = (((1 - support) * pow(p, 2)) / ((1 - support) * p + support * (1 - p))) \
    + (((1 - support) * pow(1 - p, 2)) / (support * p + (1 - support) * (1 - p)))

a = .9

R = a * R1 + (1 - a) * R0

privacy = float((1 - R) * 100)

print("User Privacy raggiunta: {}%".format(privacy))

# Stima singleton supports colonna 1

j = 1

# conto gli uni
C1_D = 0
for i in range(0, (num_clients - 1)):
    if distorted[i,j] == 1:
        C1_D += 1

# conto gli zeri
C0_D = num_clients - C1_D

# DA METTERE APPOSTO
M = [[0 for x in range(2)]for y in range(2)]
M[0][0] = p
M[0][1] = 1-p
M[1][0] = 1-p
M[1][1] = p
C_D = [[0 for x in range(2)]for y in range(1)]
C_D[0][0] = C1_D
C_D[0][1] = C0_D

C_T = np.linalg.inv(M) @ C_D
print(C_T)

