from scipy import io
from scipy.sparse import issparse
import numpy as np

d = io.loadmat('test.mat')
dataset = d['dataset']

print(issparse(dataset))
