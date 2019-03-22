import numpy as np

def estimate_singleton(distorted, p, num_clients, M):
    # colonna j
    j = 1

    # conto gli uni
    C1_D = int(sum(distorted[:, j] == 1))

    # conto gli zeri
    C0_D = num_clients - C1_D

    # calcolo C_T partendo dalla conoscenza di C_D ed M
    # inversione matrice
    M = np.linalg.inv(M)

    C_D = np.matrix([[C1_D], [C0_D]])
    C_T = np.dot(M, C_D)

    print("C_T_bad:\n {}".format(C_T))