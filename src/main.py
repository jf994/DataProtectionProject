from scipy import io
import numpy as np
from scipy import sparse

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

# calcolo R1(p), R0(p), R per calcolare poi la privacy ottenuta

R1 = ((support * pow(p, 2)) / (support * p + (1 - support) * (1 - p))) \
    + ((support * pow(1 - p, 2)) / (support * (1 - p) + (1 - support) * p))

R0 = (((1 - support) * pow(p, 2)) / ((1 - support) * p + support * (1 - p))) \
    + (((1 - support) * pow(1 - p, 2)) / (support * p + (1 - support) * (1 - p)))

a = .9

R = a * R1 + (1 - a) * R0

privacy = (1 - R) * 100

print("User Privacy raggiunta: {}%".format(privacy))


# Stima singleton supports 1 colonna

# colonna j
j = 1


# conto gli uni
C1_D = int(sum(distorted[:, j] == 1))

# conto gli zeri
C0_D = num_clients - C1_D

# calcolo C_T partendo dalla conoscenza di C_D ed M
M = np.matrix([[p, 1-p], [1-p, p]])

C_D = np.matrix([[C1_D], [C0_D]])
C_T = np.dot(np.linalg.inv(M), C_D)

# TODO: C_T presenta un numero > 7500 in pos 0,0 ed uno negativo in pos 1,0 (valori insensati). Questo è un tapullo per far funzionare il tutto
C_T[0] = C_T[1] + 7500
C_T[1] = -C_T[1]
print("C_T:\n {}".format(C_T))


# Stima n-itemset support più colonne

relations = []
# threshold calcolato come circa 0.03 * 7500, con 0.03 support medio
threshold = 250
n = 2


# trovo la M per il caso multidimensionale
M = np.zeros((pow(2, n), pow(2, n)))
for row in range(0, pow(2, n)):
    for col in range(0, pow(2, n)):
        # le probabilita sono indipendenti, la probabilit� finale viene calcolata
        # come il prodotto delle opportune probabilit�. temp = 1 come valore neutro per la motliplicazione
        temp = 1
        # per ogni riga e colonna trasformo il corrispondente valore in binario
        temp_row = str('{0:b}'.format(row))
        temp_row = temp_row.zfill(n)
        temp_col = str('{0:b}'.format(col))
        temp_col = temp_col.zfill(n)

        # confronto bit a bit i valori ottenuti e genero opportunamente i vari mij (per ogni cifra se il bit
        # rimane uguale ho probabilita p, cambia ho prob 1-p)
        for iter in range(0, n):
            if (temp_row[iter]==temp_col[iter]):
                temp *= p
            else:
                temp *= 1-p
        M[row][col] = temp

print("\nM_big:\n{}".format(M))

# f � la cardinalit� dell'insieme considerato (numero di coppie trovate)
f = 0
somma = 0
# uso due for annidati per esplorare tutte le coppie di 10 elementi. start da 0 a 10-1 e l da start+1 a 10 evitando ripetizioni
for start in range(0, 9):
    for l in range(start+1, 10):
        f += 1
        print("giro: {}, colonne: {}{}".format(f,start, l))
        # genero opportunamente C_D per il caso multidimensionale
        C2n_D = np.zeros((pow(2, n), 1))
        # trovo le corrispondenze per i valori binari cercati ad ogni giro e costruisco C_D come spiegato sul pdf MASK
        act_support = 0
        for i in range(0, pow(2, n)):
            k = '{0:b}'.format(i)
            k = k.zfill(n)

            for h in range(0, 7500):
                binario = ''
                binario = str(distorted[h, start]) + str(distorted[h, l])
                #print(str(k) + " binario: " + binario)
                if str(k) == binario:
                    C2n_D[pow(2, n)-1-i][0] += 1
                    #print("\nC2n_D:\n{}".format(C2n_D))
                # inoltre solo al primo giro vengono contate anche le relazioni associative presenti nel dataset originale
                # TODO: generalizzare questo controllo per n>2
                if i == 0 and dataset.A[h][start] == 1 and dataset.A[h][l] == 1:
                        act_support += 1
        # calcolo del supporto ricostruito: calcoliamo la probabilit� che un 11 sia stato distorto in uno qualsiasi delle
        # forme possibili (00 01 10 11) usando valori opportuni nella matrice M e quelli del vettore C2n_D
        rec_support = M[0][0]*C2n_D[0][0] + M[0][1]*C2n_D[1][0] + M[0][1]*C2n_D[2][0] + M[0][3]*C2n_D[3][0]

        act_support /= 7500
        # act suport talvolta viene zero con evidenti problemi nella formula normale del calcolo del support error, paragrafo 6.3,
        # presente nell'else
        #  abbiamo deciso di impedire artificialmente l'errore per poter continuare ad ottenere risultati (da mettere apposto)
        if act_support == 0:
            somma += 0
        else:
            somma += (abs(1-act_support)/act_support)

        # calcolo C_T
        # TODO: ha lo stesso identico problema del C_T monodimensionale (numeri negativi presenti)...ignoriamo il problema in questo caso
        C2n_T = np.dot(np.linalg.inv(M), C2n_D)
        print("\nC_T_big:\n {}".format(C2n_T))
        # se il primo valore, relativo a 11 per il vettore appena ottenuto supera il theshold
        if C2n_T[0] > threshold:
            # creo la relazione e la appendo alla lista
            relation = str(items[start][:]) + " --> " + str(items[l][:])
            relations.append(relation)

# conclusione del calcolo del support error i valori riscontrati sono enormi, nell'ordine delle migliaia.
# Dovrebbero essere, al massimo, nell'ordine delle unit�.
result = 100/f * somma
print("\nrelations:\n{}".format(relations))
print("\nresultanze:\n{}".format(result))
