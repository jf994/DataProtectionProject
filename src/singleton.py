import numpy as np

def estimate_singleton(distorted, p, num_clients):
    # colonna j
    j = 1

    # conto gli uni
    C1_D = int(sum(distorted[:, j] == 1))

    # conto gli zeri
    C0_D = num_clients - C1_D

    # calcolo C_T partendo dalla conoscenza di C_D ed M
    M = np.matrix([[p, 1 - p], [1 - p, p]])

    # USATA ROTAZIONE DI 90 GRADI INVECE CHE INVERSIONE MATRICE
    M = np.rot90(M)
    print("M:\n {}".format(M))

    C_D = np.matrix([[C1_D], [C0_D]])
    C_T = np.dot(M, C_D)

    print("C_T:\n {}".format(C_T))

def bad_estimate_singleton(distorted, p, num_clients):
    # colonna j
    j = 1

    # conto gli uni
    C1_D = int(sum(distorted[:, j] == 1))

    # conto gli zeri
    C0_D = num_clients - C1_D

    # calcolo C_T partendo dalla conoscenza di C_D ed M
    M = np.matrix([[p, 1 - p], [1 - p, p]])

    # inversione matrice
    M = np.linalg.inv(M)
    print("M_bad:\n {}".format(M))

    C_D = np.matrix([[C1_D], [C0_D]])
    C_T = np.dot(M, C_D)

    print("C_T_bad:\n {}".format(C_T))