# Progetto a cura di Fabrizio Zavanone e Jacopo Favaro

Per preparare il dataset nel formato richiesto dallo script in python, è necessario lanciare prima lo script matlab "modify_dataset.m", che salva il dataset contenuto nel file .xlsx in una matrice sparsa di 0 e 1. Lo script genera un file .mat che viene poi interpretato. Vengono inoltre salvate altre variabili di circostanza per la ricostruzione come l'identità originaria degli item.

In seguito deve essere lanciato lo script matlab "calculate_support.m" che calcola il supporto medio s0 per il dataset e lo salva nel .mat precedente (valore utile al calcolo della privacy).

Deve infine essere lanciato lo script "create_distorted.m" il quale, seguendo la procedura descritta nel paper, altera il dataset originale xorando ogni elemento con un bit casuale generato da una distribuzione di bernulli con probabilità p = 0.7 .

Lo script "apriori.py" è uno script di test per vedere il funzionamento della libreria trovata che applica, appunto, l'algoritmo Apriori.

Lo script python principale è "main.py", il quale segue i ragionamenti proposti nel paper e svolge pedissequamente tali calcoli. 
La prima parte si occupa di ricavare la privacy dovuta all'alterazione del dataset e dovrebbe essere coerente con quanto esposto nel paper.

Viene poi calcolata la stima per il supporto della singola colonna, composta da 7500 entry, che genera le prime incoerenze: il vettore risultante, che dovrebbe esprimere una stima statistica degli 1 e degli 0 presenti nella colonna in considerazione nel dataset di partenza, dà come risultato un numero maggiore degli elementi possibili (12742 circa "1" e -5242 "0", la cui somma è però coerente con i dati di partenza ovvero 7500).

Per tentare di andare avanti abbiamo assunto il secondo numero cambiato di segno come valore reale, ricavando il primo come 7500-n. Continuando poi nella stima per 2 item abbiamo calcolato la matrice M come descritto nel paragrafo 4. Abbiamo proceduto nel testare poi per i primi 10 item su tutte le possibili coppie cercando quelle relazioni che esprimessero un valore "1 1" nel dataset originario. Il risultato finale ripresenta lo stesso tipo di errore con alcuni parametri negativi e lo stesso tipo di incoerenza con la somma degli stessi che produce sempre esattamente 7500.