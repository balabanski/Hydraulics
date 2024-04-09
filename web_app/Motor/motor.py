from web_app.Motor.parameters import metadata_mot, parameter_mot_input


# Рабочий объём V(см3)
def _V(Q, n, n_ob=0.95):
    """

    :param Q: л/мин
    :param n: об/мин
    :param n_ob: float
    :return: см3
    """
    V = Q * 1000 * n_ob / n
    return V


def V():
    Q = parameter_mot_input("Q")
    n = parameter_mot_input("n")
    V_ = _V(Q, n)
    metadata_mot["V"] = round(V_, 2)
    return V_


# скорость вращения n(об/мин)
def _n(Q, V, n_ob=0.95):
    """
    :param Q: л/мин
    :param V: см3
    :param n_ob: float
    :return: об/мин
    """
    _n = Q * 1000 * n_ob / V
    return _n


def n():
    Q = parameter_mot_input("Q")
    V = parameter_mot_input("V")
    n_ = _n(Q, V)
    metadata_mot["n"] = round(n_, 1)
    return n_


# Требуемая подача Q(л/мин)
def _Q(V, n, n_ob=0.95):
    """
    :param V: см3
    :param n: об/мин
    :param n_ob: float
    :return: л/мин
    """
    _Q = V * n / (1000 * n_ob)
    return round(_Q, 1)


def Q():
    V = parameter_mot_input("V")
    n = parameter_mot_input("n")
    Q_ = _Q(V, n)
    metadata_mot["Q"] = Q_
    return Q_


# Требуемое давление(перепад давления) p(Bar)
def _p(V, M, n_meh=0.94):
    _p = M * 2 * 3.14 * 100 / (V * n_meh)
    return _p


def p():
    V = parameter_mot_input("V")
    M = parameter_mot_input("M")
    p_ = _p(V, M)
    metadata_mot["p"] = round(p_, 1)
    return p_


# вращающий момент ведомого вала(даН*м)
def _M(p, V, n_meh=0.94):
    """

    :param p: Bar
    :param V: см3
    :param n_meh: float
    :return: даН*м (деканьютон*м)
    """
    _M = p * V * n_meh / (2 * 3.14 * 100)
    return _M


def M():
    p = parameter_mot_input("p")
    V = parameter_mot_input("V")
    M_ = _M(p, V)
    metadata_mot["M"] = round(M_, 1)
    return M_


# мощность  ведомого вала P (кВт)
def _P(p, Q, n_kpd=0.84):
    _P = p * Q * n_kpd / 600
    return _P


def P():
    p = parameter_mot_input("p")
    Q = parameter_mot_input("Q")
    P_ = _P(p, Q)
    metadata_mot["P"] = round(P_, 1)
    return P_
