import numpy as np
from itertools import combinations

from calculate_M import calc_M

def estimate_n_itemset(dataset, distorted, n, p, threshold, items, relations,comb):
    # calcolo M per l'n desiderato
    M = calc_M(n, p)
    M_inv = np.linalg.inv(M)
    # print("\nM:\n{}".format(M))

    # F è la cardinalità dell'insieme degli item frequenti
    R_plus = somma = F = R_minus = 0
    new_active_items = []

    print("Livello: {}\n".format(n))
    # uso due for annidati per esplorare tutte le coppie di x elementi. first_column da 0 a x e second_column da first_column+1 ad x evitando ripetizioni
    for el_comb in comb:
        print("Colonne: {}".format(el_comb))
        # istanzio opportunamente C_D l'ultimo valore verrà ricavato per sottrazione, partirà quindi da 7500
        Cn_D = np.zeros((pow(2, n), 1))

        # trovo le corrispondenze per i valori binari cercati ad ogni giro e costruisco C_D come spiegato sul pdf MASK
        act_support = 0
        for h in range(0, 7500):
            # inoltre vengono contate anche le relazioni associative presenti nel dataset originale
            ctrl = True
            pos = 0
            # ricerco nel dataset originale gli n-itemset presenti
            binario = ""
            while pos < len(el_comb):
                # print("el_comb[pos]: {}\n".format(el_comb[pos]))
                # se uno solo dei valori è zero smetto di controllare
                if ctrl and dataset.A[h][el_comb[pos]] != 1:
                    ctrl = False
                # preparo la logica per riconoscere il numero binario, costruendo una stringa da comparare
                binario += str(distorted[h, el_comb[pos]])
                # print("bin: {}\n".format(binario))
                pos += 1
            if ctrl:
                # se tutti gli n item sono a 1 incremento il contatore
                act_support += 1
                # print("act_s_dentro_ctrl: {}".format(act_support))

            posizione = int(binario, 2)
            # print("{} --> {}\n".format(binario,posizione))
            # incremento il valore opportuno nel vettore Cn_D in posizione opportuna
            Cn_D[pow(2, n) - posizione - 1] += 1

        # calcolo C_T
        Cn_T = M_inv @ Cn_D
        print("Cn_T:\n {}\nCn_D:\n{}".format(Cn_T, Cn_D))
        # print("act_s_pre_divisione: {}".format(act_support))

        # calcolo rec_support ed act_support
        act = False
        rec = False
        act_support /= 7500
        rec_support = 0

        # uso la stima ottenuta per calcolare il rec_support
        if Cn_T[0] > 0:
            rec_support = int(Cn_T[0])/7500

        # inizio i calcoli per la stima della bontà del modello sul dataset originale
        if act_support > threshold:
            act = True
            F += 1
            # act suport talvolta viene zero con evidenti problemi nella formula normale del calcolo del support error, paragrafo 6.3,
            # presente nell'else
            # abbiamo deciso di impedire artificialmente l'errore per poter continuare ad ottenere risultati
            if act_support == 0:
                somma += 0
            else:
                somma += (abs(rec_support - act_support) / act_support)

        print("\nrec_support: {}".format(rec_support))
        print("act_s: {}".format(act_support))
        # nel caso la relazione supero il threshold e quindi sia "interessante"
        if rec_support > threshold:
            rec = True
            # creo la relazione e la appendo alla lista
            relation = ""
            for pos2, el in enumerate(el_comb):

                if n > 1:
                    relation += str(items[el][:])
                if pos2 < len(el_comb)-1:
                    relation += " --> "
                if el not in new_active_items:
                    new_active_items.append(el)
            if n > 1:
                relations.append(relation)
        # se la relazione compare nel support ricostruito ma non nell'reale ho un falso positivo
        if rec and not act:
            R_plus += 1
        # se la relazione compare nel support reale ma non nel ricostruito ho un falso negativo
        if not rec and act:
            R_minus += 1

    # CALCOLO SUPPORT ERROR
    # evito divisione per zero
    if F == 0:
        F = -1

    support_error = 100/F * somma
    print("\nsupport error:\n{}".format(support_error))

    # CALCOLO IDENTITY ERROR
    S_plus = (abs(R_plus)/F) * 100
    S_minus = (abs(R_minus)/F) * 100

    print("\nF: {}\nR_plus: {}\nR_minus: {}\nS+: {}\nS-: {}\n".format(F, R_plus, R_minus, S_plus, S_minus))
    n = n + 1

    # tra gli item che hanno superato il trashold genero nuove combinazioni per il passo successivo
    comb = combinations(new_active_items, n)

    print("n_active_items: {}".format(new_active_items))

    # chiamo la funzione per il passo successivo in maniera ricorsiva, altrimenti stampo le relazioni trovate
    if len(new_active_items) >= n:
        estimate_n_itemset(dataset, distorted, n, p, threshold, items, relations, comb)
    else:
        print("\nrelations:\n{}".format(relations))
