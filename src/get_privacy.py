def calculate_privacy(support, p):
    # calcolo R1(p), R0(p), R per calcolare poi la privacy ottenuta
    R1 = ((support * pow(p, 2)) / (support * p + (1 - support) * (1 - p))) \
        + ((support * pow(1 - p, 2)) / (support * (1 - p) + (1 - support) * p))

    R0 = (((1 - support) * pow(p, 2)) / ((1 - support) * p + support * (1 - p))) \
        + (((1 - support) * pow(1 - p, 2)) / (support * p + (1 - support) * (1 - p)))

    # a rappresenta il peso dato alla privacy di un 1 rispetto a uno 0
    a = .9

    R = a * R1 + (1 - a) * R0
    privacy = (1 - R) * 100
    print("User Privacy raggiunta: {}%".format(privacy))
