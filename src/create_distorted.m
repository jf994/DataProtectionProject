clear
clc

%% distorsione ds 500
load('dataset_500.mat');
p = .7;

distorted = [];
for i = 1:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        distorted(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end

clear dataset i items j
save('distorted_500.mat');

%% distorsione ds 5000
clear

load('dataset_5000.mat');

distorted = [];
for i = 1:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        distorted(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end

clear dataset i items j
save('distorted_5000.mat');

%% distorsione 50k

clear

load('dataset_50k.mat');

distorted = [];
for i = 1:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        distorted(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end

clear dataset i items j
save('distorted_50k.mat');

%% distorsione 500k part 1

clear

load('dataset_500k.mat');

temp = [];

load('distorted_500.mat')
temp = [temp; distorted];
load('distorted_5000.mat')
temp = [temp; distorted];
load('distorted_50k.mat')
temp = [temp; distorted];

clear distorted
%% distorsione 500k part 2


for i = 55501:size(dataset,1)
    i
    for j = 1:size(dataset,2) 
        temp(i,j) = xor(dataset(i,j),ri_complement(p)); %#ok<*SAGROW>
    end
end
fprintf('Distorsione conclusa.\n');

distorted = temp;
clear dataset i items j temp
save('distorted_500k.mat');