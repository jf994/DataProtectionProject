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

# calcolo R1(p), R0(p), R per calcolare poi la privacy ottenuta

R1 = ((support * pow(p, 2)) / (support * p + (1 - support) * (1 - p))) \
    + ((support * pow(1 - p, 2)) / (support * (1 - p) + (1 - support) * p))

R0 = (((1 - support) * pow(p, 2)) / ((1 - support) * p + support * (1 - p))) \
    + (((1 - support) * pow(1 - p, 2)) / (support * p + (1 - support) * (1 - p)))

a = .9

R = a * R1 + (1 - a) * R0

privacy = (1 - R) * 100

print("User Privacy raggiunta: {}%".format(privacy))

# Effettuiamo il mining sul ds distorto
