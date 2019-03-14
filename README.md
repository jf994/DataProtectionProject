# Progetto a cura di Fabrizio Zavanone e Jacopo Favaro

## preparazione del dataset

Per preparare il dataset nel formato richiesto dallo script in python è necessario lanciare prima lo script matlab "modify_dataset" che trasforma il file xlxs utilizzato in una matrice sparsa di 0 e 1. lo script genera un file .mat che viene poi interpretato. vengono inoltre salvate altre variabili di circostanza per la ricostruzione come l'identità originaria degli item

A seguito deve esseere lanciato lo script matlab "calculate_support.m" che calcola il supporto medio s0 per il dataset e salva nel .mat precedente, valore utile al calcolo della privacy

Deve infine essere lanciato lo script "create_distorted.m" il quale, seguendo la procedura desccritta nel paper altera il dataset originale xorando ogni elemento con un bit casuale generato da una distribuzione di bernulli con probabilità p = .7

lo script "apriori.py" è uno script di test per vedere il funzionamento della libreria trovata, di fatto poco importante


lo script python principale è main.py il quale segue i ragionamenti proposti nel paper e svolge pedissequamente tali calcoli. 
La prima parte si occupa di ricavare la privacy dovuta all'alterazione del dataset e dovrebbe essere coerente con quanto esposto nel paper.

viene poi calcolata la stima per il supporto della singola colonna, composta da 7500 entry, che genera le prime incoerenze. il vettore risultatne, che dovrebbe esprimere una stima statistica degli 1 e degli 0 presenti nella colonna in considerazione nel dataset di partenza, da come risultato un numero maggiore degli elementi possibili 12742 circa "1" e -5242 "0" (la cui somma è però coerente con i dati di partenza ovvero 7500)

per tentare di andare avanti abbiamo assunto il secondo numero cambiato di segno come valore reale ricavando il primo come 7500-n. continuando poi nella stima per 2 item abbiamo calcolato la matrice M come descritto nel paragrafo 4 e testato per le prime due colonne del dataset. il risultato finale ripresenta lo stesso tipo di errore con alcuni parametri negativi. La somma questa volta non è coerente con le dimensioni del dataset





