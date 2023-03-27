from Pump.parameters import  metadata_pump, parameter_pump_input


# рабочий объём V(см3)
def _V(Q, n= 1500, n_ob=0.95 ):
    _V= Q * 1000 / (n * n_ob)
    return round(_V, 1)

def V ():
    Q= parameter_pump_input('Q')
    n = parameter_pump_input('n')
    V_ = _V(Q,n)
    metadata_pump['V']= V_
    return V_



# подача насоса Q(л/мин)__n(об/мин)
def _Q(V, n, n_ob=0.95):
    _Q= V * n * n_ob / 1000
    return round(_Q, 1)

def Q():
    V= parameter_pump_input('V')
    n= parameter_pump_input('n')
    Q_= _Q(V, n)
    metadata_pump['Q']= Q_
    return Q_



# мощность привода P(кВт)
def _P(p, Q, n_kpd=0.82):
    _P=p * Q /(600 * n_kpd)
    return round(_P, 1)

def P():
    p= parameter_pump_input('p')
    Q= parameter_pump_input('Q')
    P_= _P(p, Q)
    metadata_pump['P']= P_
    return P_
