clear
clc
% creo dataset

customers = 500000;
items = 200;
dataset = sparse(customers,items);

for i = 1:customers
    i
    bought_items = randi([1, 20]);
    pos_vector = randi(items, bought_items,1);

    dataset(i,pos_vector) = 1;
end