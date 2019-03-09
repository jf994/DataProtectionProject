function ri_ = ri_complement(p)
%RI_COMPLEMENT Summary of this function goes here
%   Detailed explanation goes here
    random = randi([1 10]);
    if random > p
        ri_ = 1;
    else
        ri_ = 0;
    end
end

