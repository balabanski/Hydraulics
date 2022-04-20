# Требуемая подача Q(л/мин)_V(см3) _n(об/мин)
def Q(V, n, n_ob=0.95):
    """

    :param V: см3
    :param n: об/мин
    :param n_ob: float
    :return: л/мин
    """
    _Q= V * n / (1000 * n_ob )
    return _Q

# скорость вращения n(об/мин)
def n(Q, V,  n_ob=0.95):
    """

    :param Q: л/мин
    :param V: см3
    :param n_ob: float
    :return: об/мин
    """
    _n = Q * 1000 * n_ob / V
    return _n

# вращающий момент ведомого вала             , _d_p(Bar)
def M(d_p, V, n_meh=0.94):
    _M = d_p * V * n_meh / (2 * 3.14 *100)
    return _M
    
# мощность  ведомого вала P (кВт)
def P(d_p, Q, n_kpd=0.84):
    _P = d_p * Q * n_kpd / 600
    return _P
