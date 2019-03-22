import numpy as np

def estimate_3_itemset(dataset, distorted, n, M, threshold, items, relations):
    # f è la cardinalità dell'insieme considerato (numero di coppie trovate)
    R = somma = F = 0
    # uso due for annidati per esplorare tutte le coppie di 10 elementi. first_column da 0 a 10-1 e l da first_column+1 a 10 evitando ripetizioni
    # TODO: calcolo di F ed R è corretto?
    # TODO: processo molto lento anche dopo ottimizzazioni
    # TODO: dare nomi sensati alle variabili dei for
    for first_column in range(0, 3):
        for second_column in range(first_column+1, 4):
            for third_column in range(second_column+1, 5):

                print("colonne: {} {} {}".format(first_column, second_column, third_column))
                # genero opportunamente C_D per il caso multidimensionale
                C2n_D = np.zeros((pow(2, n), 1))
                C2n_D[0] = 7500
                # trovo le corrispondenze per i valori binari cercati ad ogni giro e costruisco C_D come spiegato sul pdf MASK
                act_support = 0
                for i in range(0, pow(2, n)-1):
                    k = '{0:b}'.format(i)
                    k = k.zfill(n)

                    for h in range(0, 7500):

                        # inoltre solo al primo giro vengono contate anche le relazioni associative presenti nel dataset originale
                        # TODO: generalizzare questo controllo per n>2
                        if i == 0:
                            if dataset.A[h][first_column] == 1 and dataset.A[h][second_column] == 1 and dataset.A[h][third_column] == 1:
                                act_support += 1
                        binario = ''
                        binario = str(distorted[h, first_column]) + str(distorted[h, second_column]) + str(distorted[h, third_column])
                        # print(str(k) + " binario: " + binario)
                        if str(k) == binario:
                            C2n_D[pow(2, n) - 1 - i][0] += 1

                            # ottimizzazione per fare meno conti (11 in distorted è sicuramente la classe più frequente)
                            C2n_D[0] -= 1

                # calcolo C_T
                # USATA ROTAZIONE DI 90 GRADI INVECE CHE INVERSIONE MATRICE
                C2n_T = np.dot(np.rot90(M), C2n_D)
                print("\nC_T_big:\n {}".format(C2n_T))
                # se il primo valore, relativo a 11 per il vettore appena ottenuto supera il theshold, abbiamo un itemset frequente

                R += 1
                # calcolo del supporto ricostruito: calcoliamo la probabilità che un 11 sia stato distorto in uno qualsiasi delle
                # forme possibili (00 01 10 11) usando valori opportuni nella matrice M e quelli del vettore C2n_D (paragrafo 5.1)
                F = act_support
                act_support /= 7500
                rec_support = 0
                for c in range (0,pow(2,n)):
                    rec_support += M[0][c] * C2n_D[c][0]
                rec_support /= 7500
                # NOSTRA OTTIMIZZAZIONE
                # riduciamo i calcoli computando il rec support in questa maniera
                # rec_support = float(C2n_T[0]) / 7500
                print("\nrec_support: {}\n".format(rec_support))
                if rec_support > threshold:
                    # act suport talvolta viene zero con evidenti problemi nella formula normale del calcolo del support error, paragrafo 6.3,
                    # presente nell'else
                    #  abbiamo deciso di impedire artificialmente l'errore per poter continuare ad ottenere risultati (da mettere apposto)
                    if act_support == 0:
                        somma += 0
                    else:
                        somma += (abs(rec_support - act_support) / act_support)
                    print("\nrel_s: {}, act_s: {}\nC2n_D:\n{}".format(rec_support, act_support, C2n_D))
                    # creo la relazione e la appendo alla lista
                    relation = str(items[first_column][:]) + " --> " + str(items[second_column][:]) + " --> " + str(items[third_column][:])
                    relations.append(relation)

    # conclusione del calcolo del support error i valori riscontrati sono enormi, nell'ordine delle migliaia.
    # Dovrebbero essere, al massimo, nell'ordine delle unità

    # CALCOLO SUPPORT ERROR
    # TODO: support_error viene un numero enorme

    if F == 0:
        F = -1

    support_error = 100/F * somma
    print("\nrelations:\n{}".format(relations))
    print("\nsupport error:\n{}".format(support_error))

    # CALCOLO IDENTITY ERROR

    S_plus = (abs(R - F)/F) * 100
    S_minus = (abs(F - R)/F) * 100

    print("\nF: {}\nR: {}\nS+: {}\nS-: {}\n".format(F, R, S_plus, S_minus))