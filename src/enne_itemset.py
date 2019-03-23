import numpy as np
from itertools import combinations

from calculate_M import calc_M

def estimate_n_itemset(dataset, distorted, n, p, threshold, items, relations,comb):
    # calcolo M per l'n desiderato
    M = calc_M(n, p)
    M_inv = np.linalg.inv(M)
    # print("\nM:\n{}".format(M))

    # F è la cardinalità dell'insieme considerato (numero di coppie trovate)
    R_plus = somma = F = R_minus = 0
    new_active_items = []

    bin_list = []
    for i in range(0, pow(2, n)):
        k = '{0:b}'.format(i)
        k = k.zfill(n)
        bin_list.append(k)

    print("Livello: {}\n".format(n))
    # uso due for annidati per esplorare tutte le coppie di x elementi. first_column da 0 a x e second_column da first_column+1 ad x evitando ripetizioni
    for el_comb in comb:

        print("Colonne: {}".format(el_comb))
        # genero opportunamente C_D per il caso multidimensionale
        Cn_D = np.zeros((pow(2, n), 1))
        Cn_D[pow(2, n)-1] = 7500
        # trovo le corrispondenze per i valori binari cercati ad ogni giro e costruisco C_D come spiegato sul pdf MASK
        act_support = 0
        for i in range(1, pow(2, n)):

            for h in range(0, 7500):

                # inoltre solo al primo giro vengono contate anche le relazioni associative presenti nel dataset originale
                if i == 1:
                    ctrl = True
                    pos = 0
                    while pos < len(el_comb) and ctrl:
                        # print("el_comb[pos]: {}\n".format(el_comb[pos]))
                        if dataset.A[h][el_comb[pos]] != 1:
                            ctrl = False
                        pos += 1
                    if ctrl:
                        act_support += 1
                        # print("act_s_dentro_ctrl: {}".format(act_support))
                binario = ""
                for pos1, el in enumerate(el_comb):
                    binario += str(distorted[h, el])
                # print("binario: {}\n".format(binario))
                if str(bin_list[i]) == binario:
                    Cn_D[pow(2, n) - i - 1] += 1
                    # ottimizzazione per fare meno conti (11 in distorted è sicuramente la classe più frequente)
                    Cn_D[pow(2, n)-1] -= 1

        # calcolo C_T
        Cn_T = M_inv @ Cn_D
        # print("C_T_2-itemset:\n {}\nCn_D:\n{}".format(Cn_T, Cn_D))
        # print("act_s_pre_divisione: {}".format(act_support))
        # calcolo rec_support ed act_support
        act_support /= 7500

        act = False
        rec = False
        rec_support = 0
        # uso la stima fatta per ottenere il rec_support
        if Cn_T[0] > 0:
            rec_support = int(Cn_T[0])/7500

        if act_support > threshold:
            act = True
            F += 1
            # act suport talvolta viene zero con evidenti problemi nella formula normale del calcolo del support error, paragrafo 6.3,
            # presente nell'else
            #  abbiamo deciso di impedire artificialmente l'errore per poter continuare ad ottenere risultati
            if act_support == 0:
                somma += 0
            else:
                somma += (abs(rec_support - act_support) / act_support)

        print("\nrec_support: {}".format(rec_support))
        print("act_s: {}".format(act_support))
        if rec_support > threshold:
            rec = True
            # creo la relazione e la appendo alla lista
            relation = ""
            for pos2, el in enumerate(el_comb):
                relation += str(items[el][:])
                if pos2 < len(el_comb)-1:
                    relation += " --> "
                if el not in new_active_items:
                    new_active_items.append(el)
            relations.append(relation)
        if rec and not act:
            R_plus += 1
        if not rec and act:
            R_minus += 1

    # CALCOLO SUPPORT ERROR
    # evito divisione per zero
    if F == 0:
        F = -1

    support_error = 100/F * somma
    print("\nsupport error:\n{}".format(support_error))

    # CALCOLO IDENTITY ERROR
    S_plus = (abs(R_plus - F)/F) * 100
    S_minus = (abs(F - R_minus)/F) * 100

    print("\nF: {}\nR_plus: {}\nR_minus: {}\nS+: {}\nS-: {}\n".format(F, R_plus, R_minus, S_plus, S_minus))
    n = n + 1
    comb = combinations(new_active_items, n)

    print("n_active_items: {}".format(new_active_items))

    if len(new_active_items) >= n:
        estimate_n_itemset(dataset, distorted, n, p, threshold, items, relations, comb)
    else:
        print("\nrelations:\n{}".format(relations))
