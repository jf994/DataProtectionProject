clear
clc

% faccio distorsione dataset
load('dataset.mat');
% probabilità
p = .9;

% applico la formula della distorsione
distorted = [];
for i = 1:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        distorted(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end

% salvo il tutto più numero massimo di uni presenti in riga
clear dataset i j text
max_ones = full(max(sum(distorted,2)));

save('distorted.mat');