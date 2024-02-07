from math import sqrt
from pathlib import Path
from web_app.Cylinder.parameters import  metadata, name_par_cyl, parameter_cyl_input, \
    reference_for_d1, reference_for_d2
from web_app.Cylinder.options import option_input_cyl, insert_image, arrangement, direction, dif_or_no



# функция для расчета площади поршня  (см2)
def F_circle(d):
        f=3.1416 * d**2 / (4*100)   #см2
        f=round(f,3)
        return f

# функция для расчета  площади кольцевого сечения  (см2)
def F_ring(d, d2):
    f = (d**2  -  d2**2 )*0.786 / 100       #см2
    f=round(f,3)
    return f

def func_F_with_JSON_file( key_d, *args):
    def _F_with_JSON_file():
        if key_d == 'd1':
            d = parameter_cyl_input(key_d, reference = reference_for_d1)# ввод параметра и перезапись файла
        else:
            d = parameter_cyl_input(key_d, reference = reference_for_d2)
        if len(args)==0:
            f=F_circle(d)
            return f
        if len(args)==1:
            key_d2 = args[0]
            d2 = parameter_cyl_input(key_d2, reference = reference_for_d2)
            f = F_ring(d, d2)
            return f
    return _F_with_JSON_file

'''площадь поршня  (см2)-  расчет и запись параметров  '''
F1 = func_F_with_JSON_file('d1')

'''пплощадь кольцевого сечения  (см2)-  расчет и запись параметров  '''
F2 = func_F_with_JSON_file('d1', 'd2')

'''площадь штока (при дифференциальной схеме)  (см2)- расчет и запись параметров'''
F_diff = func_F_with_JSON_file('d2')



def _V1(L1, d1,):
    F=F_circle(d1)        #л
    _V1 = L1*F/10000
    return round(_V1,2)

def _V2(L2, d1, d2):
    F = F_ring(d1,d2)      #л
    _V2 = L2*F/10000
    return round(_V2,2)


def func_V_wiht_JSON_file(func, key_V, key_L, *keys_d):
    def _V_wiht_JSON_file():
        args = []
        for i in keys_d:
            par=parameter_cyl_input(i)
            args.append(par)
        L = parameter_cyl_input(key_L)
        V=func(L, *args)
        metadata[key_V]=round(V, 2)
        return V
    return _V_wiht_JSON_file


'''при дифференц.семе подключения- требуемый объём маcла'''
V1_diff = func_V_wiht_JSON_file(_V1, "V1_diff", "L1", "d2")

'''объём поршневой полости'''
V1 = func_V_wiht_JSON_file(_V1, "V1", "L1", "d1")

'''объём штоковой полости'''
V2 = func_V_wiht_JSON_file(_V2, "V2", "L2", "d1", "d2")


# теоретическое время хода поршня  (с)------------------------------------------
def t_theor_(Q, L, F, n_ob = 0.95):
    t_theor = F * L *6 / (Q * n_ob * 1000)
    return t_theor

'''
from debug import debug
@debug
'''
def t_teor(func_F, key_Q, key_L, key_t):
    def _t_teor():
        Q= parameter_cyl_input(key_Q)
        L= parameter_cyl_input(key_L)
        F= func_F()
        _t= round(t_theor_(Q, L, F), 1)
        metadata[key_t] = _t
        return _t
    return _t_teor

t1= t_teor(F1, 'Q1', 'L1', 't1')
t2= t_teor(F2, 'Q2', 'L2', 't2')
t1_diff= (F_diff, 'Q_diff', 'L1', 't1_diff')



# функция для расчета  фактиеской скорости  (м/с)
# _L-ход(мм)
def v_fact(L, t ):
    v_par=L/(t * 1000)
    v_par= round(v_par,3)
    return v_par


def func_v_fact_with_dict( func_F, key_L, key_t, key_v):
    def _v_with_dict():
        def Q(F, v, n_ob = 0.95):
            Q=F *v * 6 / n_ob   # л/мин
            q=round(Q,2)
            return q
        L = parameter_cyl_input(key_L)
        t = parameter_cyl_input(key_t)
        F=func_F()
        v=v_fact(L, t)
        Q = Q(F, v)
        metadata[key_v] = v
        return '{} = {}ceк.\n{} = {}м/сек\nQ = {}л/мин'.format(key_t, t, key_v, v, Q)
    return _v_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
v1_fact  = func_v_fact_with_dict(F1, "L1", "t1_fact", "v1_fact")
v2_fact = func_v_fact_with_dict(F2, "L2", "t2_fact", "v2_fact")
v1_diff_f = func_v_fact_with_dict(F_diff, "L1", "t1_fact", "v1_diff_f")


# функция для расчета  теоретической  скорости  (м/с)
# _Q(л/мин)_F(см2)
def v_theor(F, Q, n_ob=0.95):
    v = Q  / (F * 6 * n_ob)
    return v

def func_v_theoretic_with_dict(func_F, key_Q,  key_v):
    def _v_theoretic_with_dict():
        F = func_F()
        Q = parameter_cyl_input(key_Q)
        v = v_theor(F, Q)
        metadata[key_v] = round(v, 2)
        return v
    return _v_theoretic_with_dict
v1 = func_v_theoretic_with_dict(F1, 'Q1', 'v1')
v1_diff = func_v_theoretic_with_dict(F_diff, 'Q1_diff', 'v1_diff')
v2 = func_v_theoretic_with_dict(F2, 'Q2', 'v2')


#функция для вычисления требуемого(фактического) расхода (л/мин)
# _F-площадь(см3) _v -скорость (м/сек)
def Q(F, v, n_ob = 0.95):
    Q=F *v * 6 / n_ob   # л/мин
    q=round(Q,2)
    return q


def func_Q_with_dict(func_F, funk_v, key_v, key_q):
    def Q_with_dict():
        F = func_F()
        v = parameter_cyl_input(key_v)
        _Q= Q(F, v, n_ob = 0.95)
        metadata[key_q]=_Q
        return _Q
    return Q_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
Q1 = func_Q_with_dict(F1, v1, 'v1','Q1') # требуемый расход при выдвижении штока
Q2 = func_Q_with_dict(F2, v2, 'v2','Q2') # требуемый расход при втягивании штока
Q1_diff = func_Q_with_dict(F_diff, v1, 'v1_diff','Q1') # (при дифференциальной схеме)требуемый расход при выдвижении штока


# сила (кН)   (m = тн, а=м/с2)
def P(m, g, a=0.1,):
    _P= m *(a + g)
    return _P             # кН


# функция для вычисления требуемого усилия
def func_P_with_dict(key_P):
    def _P_with_dict():
        _P = 0
        var_P = option_input_cyl(*arrangement)
        m = parameter_cyl_input('m')
        _a = parameter_cyl_input('a')
        g= None
        if var_P == arrangement[0]:
            g = 0
        elif var_P == arrangement[1]:
            g= 9.8
        _P=round(P(m, g, _a), 2)

        metadata[key_P] = _P
        return _P
    return _P_with_dict

P1  = func_P_with_dict('P1')
P1_diff = func_P_with_dict('P1')
P2  = func_P_with_dict('P2')


def p(P,F):
    '''
    вычисление требуемого давления  (P=кН, F=см2)
    (без учета потерь трения)
    '''
    _p = P * 100/F   # Н/см2  или Bar
    return round( _p,1)


def func_p_with_dict(func_F, func_P, key_p, key_P):
    def _p_with_dict():
        F = func_F()
        options = ('ввести значение усилия', 'вычислить значение усилия')
        var_P = option_input_cyl(*options)
        _P = None
        if var_P == options[0]:
            _P = parameter_cyl_input(key_P)
        elif var_P == options[1]:
            _P = func_P()

        _p = p(_P, F)
        metadata[key_p] = _p
        return _p
    return _p_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
p1 = func_p_with_dict(F1,P1,'p1', 'P1') # требуемое давление при выдвижении штока
p1_dif = func_p_with_dict(F_diff,P1,'p1', 'P1')
p2 = func_p_with_dict(F2,P2,'p2', 'P2') # требуемое давление при втягивании штока


nomogramma_compiled = None
def selection_D_and_d():
    '''
    подбор диаметра поршня (и штока) исходя из заданного давления и силы  (мм)
    диаметр штока d2  ЗАДАЁМ исходя из нагрузги и длины штока по номогррамме для
    определения диаметра штока
    '''

    var_p = option_input_cyl(dif_or_no[1], *direction)
    key_p = None
    key_P = None

    nomogramma_path= str(Path(Path.cwd(),'Cylinder', 'images', 'Nomogramma_.png'))
    global nomogramma_compiled
    if not nomogramma_compiled :
        nomogramma_compiled = insert_image(nomogramma_path)

    if var_p == direction[0] or var_p == dif_or_no[1]:
        key_p = 'p1'
        key_P = 'P1'
    elif var_p == direction[1]:
        key_p = 'p2'
        key_P = 'P2'

    p = parameter_cyl_input(key_p)
    P = None
    options_P = ('ввести значение усилия', 'вычислить значение усилия')
    var_P= option_input_cyl(*options_P)
    if var_P == options_P[0]:
        P=parameter_cyl_input(key_P)
    elif var_P == options_P[1]:
        P = func_P_with_dict(key_P)()
        metadata[key_P]=P
        P=parameter_cyl_input(key = key_P, message= 'в результате вычисления')

    message_for_d1 = 'В соответствии с заданным усилием при выдвижении ' \
                     'штока {}кН min значение параметра\n'.format(metadata.get('P1'))

    _reference = 'задаём диаметр штока d2 исходя из усилия выдвижения ' \
                                 '{} (кН) и условной длины штока (ход поршня определён {}(мм)) по номогррамме.' \
                                 '\n'.format(metadata.get('P1'),
                                             metadata.get('L1', metadata.get('L2')))
    arg_for_d2 = dict(reference = _reference + reference_for_d2,
                      image_compiled = nomogramma_compiled)

    F = P*100/p   #  определяем требуемую площадь см2(Н/см2==10Bar

    if var_p == direction[0]:
        d = sqrt(F * 100 / 0.785)
        metadata['d1'] = d

        d = parameter_cyl_input(key = 'd1',
                            message= message_for_d1,
                            reference= reference_for_d1
                            )
        parameter_cyl_input(key = 'd2', **arg_for_d2)

    elif var_p  == dif_or_no[1]:
        d = sqrt(F * 100 / 0.785)
        metadata['d2'] = d

        d = parameter_cyl_input(key = 'd2',
                            message= 'при дифференциальной схеме рабочей площадью '
                                     'является площадь штока.\n'+ message_for_d1,
                                    **arg_for_d2)


    elif var_p == direction[1]:
        d2 = parameter_cyl_input(key = 'd2', **arg_for_d2)
        d = sqrt(( F * 100  / 0.786 ) + d2**2)
        msg_for_d2 = 'если диаметр штока определён значением {} мм и\n{} опрелен' \
                     ' значением {}кН, ' \
                     'то min значение'.format(metadata.get('d2'), name_par_cyl.get('P2'), metadata.get('P2'))

        if metadata.get('P2') < metadata.get('P1', 0) and d < metadata['d1']:
            d1 = metadata.get('d1')
            metadata['d1'] = d
            msg_for_d2 = 'ВНИМАНИЕ:\nтак как {} БОЛЬШЕ чем {}\n ' \
                        'то необходимо учесть ранее заданный d1(мм)- диаметр поршня,' \
                        'равный {}\n\n'.format(name_par_cyl.get('P1'), name_par_cyl.get('P2') , d1) + msg_for_d2
        else:
            metadata['d1'] = d

        parameter_cyl_input(key = 'd1',
                        message= msg_for_d2,
                        reference= reference_for_d1)
    return 'диаметр поршня d1 = {}\n диаметр штока d2 = {}'.format(metadata.get('d1'), metadata.get('d2'))

