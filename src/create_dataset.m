clear
clc
%% creo dataset 500k

customers = 500000;
items = 200;
dataset = sparse(customers,items);

for i = 1:customers
    i
    bought_items = randi([1, 20]);
    pos_vector = randi(items, bought_items,1);

    dataset(i,pos_vector) = 1;
end

clear bought_items customers i pos_vector

save('dataset_500k.mat');

%% creo ds 500

temp = dataset;
dataset = [];
dataset = sparse(500,items);

dataset = temp(1:500,:);

save('dataset_500.mat');

%% creo ds 5000

dataset = [];
dataset = sparse(5000,items);

dataset = temp(501:5500,:);

save('dataset_5000.mat');

%% creo ds 50k

dataset = [];
dataset = sparse(50000,items);

dataset = temp(5501:55500,:);

save('dataset_50k.mat');