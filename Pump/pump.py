

# подача насоса Q(л/мин)_V(см3)_n(об/мин)
def Q(V, n, n_ob=0.95):
    Q= V * n * n_ob / 1000
    return Q

# мощность привода P(кВт)
def P(p, Q, n_kpd=0,82):
    P=p * Q /(600 * n_kpd)
    return P


