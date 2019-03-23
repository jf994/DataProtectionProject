import numpy as np

def calc_M(n, p):
    M = np.zeros((pow(2, n), pow(2, n)))
    # calcolo tutti i valori di M(row,col)
    for row in range(0, pow(2, n)):
        for col in range(0, pow(2, n)):
            # le probabilita sono indipendenti, la probabilità finale viene calcolata
            # come il prodotto delle opportune probabilità. temp = 1 come valore neutro per la motliplicazione
            temp = 1
            # per ogni riga e colonna trasformo il corrispondente valore in binario
            temp_row = str('{0:b}'.format(row))
            temp_row = str(temp_row.zfill(n))
            temp_col = str('{0:b}'.format(col))
            temp_col = str(temp_col.zfill(n))

            # confronto bit a bit i valori ottenuti e genero opportunamente i vari mij (per ogni cifra se il bit
            # rimane uguale ho probabilita p, cambia ho prob 1-p)
            for iter in range(0, n):
                if (temp_row[iter] == temp_col[iter]):
                    temp *= p
                else:
                    temp *= 1 - p
            M[row][col] = temp

    return M
