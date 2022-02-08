# Требуемая подача Q(л/мин)_V(см3) _n(об/мин)
def Q(V, n, n_ob=0,95):
    Q= V * n / (1000 * n_ob )
    return Q

# скорость вращения n(об/мин)
def n(Q, V,  n_ob=0,95):
    n = Q * 1000 * n_ob / V
    return n

# вращающий момент ведомого вала             , _d_p(Bar)
def M(d_p, V, n_meh=0.94):
    M = d_p * V * n_meh / (2 * 3.14 *100)
    return M
    
# мощность  ведомого вала P (кВт)
def P(d_p, Q, n_kpd=0.84):
    P = d_p * Q * n_kpd / 600
    return p
