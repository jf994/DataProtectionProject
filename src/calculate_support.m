clear
clc

load('dataset.mat');

average_bought = round(sum(sum(dataset)) / size(dataset,1));
support = full(average_bought / size(items,1));

clear average_bought
save('dataset.mat');