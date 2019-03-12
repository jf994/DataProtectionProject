clear
clc

[num, text, raw] = xlsread('../docs/store_data.xlsx');
text = text(2:end-1,:);
clear raw num

% prendo tutti gli elementi singoli presenti all'interno del dataset
items = text(1,:);

for i=2:size(text,1)
    for j=1:size(text,2)
        k = 1;
        flag = false;
        while k < length(items) + 1
            if strcmp(items(k), text(i,j)) || strcmp("", text(i,j))
                flag = true;
                break;
            end
            k = k + 1;
        end
        
        if ~flag
            items = [items text(i,j)];
        end
    end
end

% creo il dataset binario
items = sort(items);
dataset = sparse(size(text,1), length(items));

for i=1:size(text,1)
    dataset(i,:) = ismember(items, text(i,:));
end

clear flag i j k

items = char(items);
text = char(text);
max_ones = full(max(sum(dataset,2)));

save('dataset.mat');