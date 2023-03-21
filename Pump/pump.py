
# рабочий объём V(см3)
def _V(Q, n= 1500, n_ob=0.95 ):
    _V= Q * 1000 / (n * n_ob)
    return _V

# подача насоса Q(л/мин)__n(об/мин)
def _Q(V, n, n_ob=0.95):
    _Q= V * n * n_ob / 1000
    return _Q

# мощность привода P(кВт)
def _P(p, Q, n_kpd=0.82):
    _P=p * Q /(600 * n_kpd)
    return _P
