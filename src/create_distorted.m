clear
clc

% distorsione dataset
load('dataset.mat');
p = .7;

distorted = [];
for i = 1:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        distorted(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end

clear dataset i j text
max_ones = full(max(sum(distorted,2)));

save('distorted.mat');