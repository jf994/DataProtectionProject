function ri_ = ri_complement(p)
% RI_COMPLEMENT calcola il complemento di ri basandosi sulla probabilità
% passata
    % applico la formula derivata dal pdf MASK, paragrafo 3.1
    random = randi([1 10]);
    if random > p
        ri_ = 1;
    else
        ri_ = 0;
    end
end

