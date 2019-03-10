clear
clc

load('dataset_500k.mat');

average_bought = round(sum(sum(dataset)) / size(dataset,1));
support = full(average_bought / items);

clear average_bought
save('dataset_500k.mat');