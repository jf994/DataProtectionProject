clear
clc
% calcolo il supporto medio s0, formula derivata dal pdf MASK paragrafo 3.2
% in fondo
load('dataset.mat');

average_bought = round(sum(sum(dataset)) / size(dataset,1));
support = full(average_bought / size(items,1));

clear average_bought
save('dataset.mat');