# Progetto a cura di Fabrizio Zavanone e Jacopo Favaro

## Risultati

### Threshold 0.025 (4h terminato)

#### 1-itemset 

F = 46 ; ro = 6.08 ; sigma- = 8.69 ; sigma+ = 4.34

#### 2-itemset 

F = 27 ; ro = 7.19 ; sigma- = 11.11 ; sigma+ = 11.11

#### 3-itemset

F = 0 ; ro = 0 ; sigma- = 0 ; sigma+ = 0

### Threshold 0.01 (23h NON terminato)

#### 1-itemset 

F = 75 ; ro = 12.51 ; sigma- = 8 ; sigma+ = 12

#### 2-itemset 

F = 165 ; ro = 12.55 ; sigma- = 15.75 ; sigma+ = 14.54

#### 3-itemset

F = ND ; ro = ND ; sigma- = ND ; sigma+ = ND

## Problemi riscontrati

1) In "main.py", file che sostanzialmente contiene tutto il procedimento mostrato nel paper, abbiamo riscontrato problemi relativamente al calcolo di C_T partendo dalla conoscenza di C_D (sia per quanto riguarda il caso monodimensionale che per quello multidimensionale). C_T ottenuto tramite prodotto tra l'inversa di M (opportunamente creata) e C_D, dà in output valori numerici insensati. Otteniamo di tanto in tantpo valori negativi.

2) act_support, calcolato in "main.py", relativo alla formula presentata nel paragrafo 6.3 del pdf talvolta viene zero generando una divisione per zero (risolto settando a zero per quel giro il risultato di (rec_support-act_support/at_support) )

3) Come ricavare f per il calcolo support error (paragrafo 6.3)? L'abbiamo interpretata come il numero di tutte le possibili combinazioni di n elementi (vedi "main.py")

4) R ed F per l'identity error (paragrafo 6.3) sono il numero di elementi presenti rispettivamente nel C_T ricostruito col metodo di cui al punto uno (M^-1 * C_D) e del C_T "vero" che superano un certo threshold? (tentativo di implementazione in "main.py")

5) Lentezza estrema del codice (anche dopo l'applicazione delle ottimizzazioni descritte nel paper)

6) Nel calcolo del support error otteniamo un valore enorme. Da cosa può dipendere?


## Funzionamento generale 

Per preparare il dataset nel formato richiesto dallo script in python, è necessario lanciare prima lo script matlab "modify_dataset.m", che salva il dataset contenuto nel file .xlsx in una matrice sparsa di 0 e 1. Lo script genera un file .mat che viene poi interpretato. Vengono inoltre salvate altre variabili di circostanza per la ricostruzione come l'identità originaria degli item.

In seguito deve essere lanciato lo script matlab "calculate_support.m" che calcola il supporto medio s0 per il dataset e lo salva nel .mat precedente (valore utile al calcolo della privacy).

Deve infine essere lanciato lo script "create_distorted.m" il quale, seguendo la procedura descritta nel paper, altera il dataset originale xorando ogni elemento con un bit casuale generato da una distribuzione di bernulli con probabilità p = 0.9 .

Lo script python principale è "main.py", il quale segue i ragionamenti proposti nel paper e svolge pedissequamente tali calcoli attraverso l'implementazione di alcune funzioni. 
La prima parte si occupa di ricavare la privacy dovuta all'alterazione del dataset e dovrebbe essere coerente con quanto esposto nel paper.
Vengono poi calcolate, tramite l'utilizzo di una funzione ricorsiva, tutte le relazioni associative relative a tutti gli n itemset possibili sul dataset ricostruito a partire dalla conoscenza di quello distorto e del fattore di distorsione p. Durante questi calcoli si presentano talvolta valori negativi all'interno di alcuni contatori, per non bloccare il progetto abbiamo deciso di ignorare questi errori e di considerarli come refusi di calcolo.