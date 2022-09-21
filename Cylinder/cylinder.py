from math import sqrt
from pathlib import Path
from Cylinder.parameters import c, messages, w_file, parameter_input, option_input,insert_image


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

def func_F_with_dict( key_d, *args):
    def _F_with_dict():
        parameter_input(key_d)# ввод параметра и перезапись файла
        d = c.get(key_d, 0)
        if len(args)==0:
            f=F_circle(d)
            return f
        if len(args)==1:
            key_d2 = args[0]
            parameter_input(key_d2)
            d2 = c.get(key_d2, 0)
            f = F_ring(d, d2)
            return f
    return _F_with_dict

'''площадь поршня  (см2)-  расчет и запись параметров  '''
F1 = func_F_with_dict('d1')

'''пплощадь кольцевого сечения  (см2)-  расчет и запись параметров  '''
F2 = func_F_with_dict('d1', 'd2')

'''площадь штока (при дифференциальной схеме)  (см2)- расчет и запись параметров'''
F_diff = func_F_with_dict('d2')


# функция для расчета  теоретической  скорости  (м/с)
# _Q(л/мин)_F(см2)
def v_t(F, Q):
    v = Q  / (F * 6)
    return v


# функция для расчета  фактиеской скорости  (м/с)
# _L-ход(мм)
def v(L, t ):
    v_par=L/(t * 1000)
    v_par= round(v_par,3)
    return v_par


def func_v_with_dict(func_v, key_L, key_t, key_v):
    def _v_with_dict():
        parameter_input(key_L)
        parameter_input(key_t)
        L = c.get(key_L, 0)
        t = c.get(key_t, 0)
        v=func_v(L, t)
        c[key_v] = v
        w_file()
        return v
    return _v_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
v1  = func_v_with_dict(v,  "L1",  "t1","v1")
v2 = func_v_with_dict(v, "L2", "t2", "v2")


#функция для вычисления требуемого(фактического) расхода (л/мин)
# _F-площадь(см3) _v -скорость (м/сек)
def Q(F, v, n_ob = 0.95):
    Q=F *v * 6 / n_ob   # л/мин
    q=round(Q,2)
    return q


def func_Q_with_dict(func_F,funk_Q,  funk_v, key_v, key_q):
    def Q_with_dict():
        F = func_F()
        parameter_input(key_v)
        v = c.get(key_v,0)
        if v == 0:
            funk_v()
            v = c.get(key_v)
        q=funk_Q(F, v, n_ob = 0.95)
        c[key_q]=q
        w_file()
        return q
    return Q_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
Q1 = func_Q_with_dict(F1,Q, v1, 'v1','Q1') # требуемый расход при выдвижении штока
Q2 = func_Q_with_dict(F2,Q, v2, 'v2','Q2') # требуемый расход при втягивании штока
Q1_diff = func_Q_with_dict(F_diff,Q, v1, 'v1','Q1') # (при дифференциальной схеме)требуемый расход при выдвижении штока


# сила (кН)   (m = тн, а=м/с2)
def P(m, a=0, g=9.8):
    _P= a * m + (g * m)
    return _P             # кН


# функция для вычисления требуемого усилия
def func_P_with_dict(key_P):
    def _P_with_dict():
        _P = 0
        options = ("подъём груза", "горизональное перемещение")
        var_P = option_input(*options)
        parameter_input('m')
        m = c.get('m',0)
        parameter_input('a')
        _a = c.get('a',0)

        if var_P == "подъём груза":
            try:
                 _P=round(P(m ,_a ),2)
            except:
                 _P=round(P(m ), 2)
            c['P_var'] = "vertical movement"
        elif var_P == "горизональное перемещение":
            _P=round(P(m, _a, g=0), 2)
            c['P_var'] = "horizontal movement"
        else:
            print('че то не так - не задана опция давления , var_P == {}'.format(var_P))
        c[key_P] = _P
        w_file()
        return _P
    return _P_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
P1  = func_P_with_dict('P1')
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
        var_P = option_input(*options)
        if var_P == options[0]:
           parameter_input(key_P)
           _P = c.get(key_P,0)
        elif var_P == options[1]:
            _P = func_P()
        else:
            print('че то не так - не задана опция давления , var_P == {}'.format(var_P))
        _p = p(_P, F)
        c[key_p] = _p
        w_file()
        return _p
    return _p_with_dict
# функции фабрики закрытия - для вызова ввести   NameFunc()
p1 = func_p_with_dict(F1,P1,'p1', 'P1') # требуемое давление при выдвижении штока
p2 = func_p_with_dict(F2,P2,'p2', 'P2') # требуемое давление при втягивании штока


image_compiled = None
def selection_D_and_d():
    '''
    подбор диаметра поршня (и штока) исходя из заданного давления и силы  (мм)
    диаметр штока d2  ЗАДАЁМ исходя из нагрузги и длины штока по номогррамме для
    определения диаметра штока
    '''
    options = ('выход штока (давление в поршневой полости)',
               'втягивание штока (давление в штоковой полости)' )
    var_p = option_input(*options)
    var_p1 = None
    key_p = None
    key_P = None
    options_p1 = None
    image_path= str(Path(Path.cwd(),'Cylinder','images', 'Nomogramma_.png'))
    global image_compiled
    if not image_compiled :
        image_compiled = insert_image(image_path)
    if var_p == options[0]:
        options_p1 = ('обычная схема подключения', 'дифференциальная схема подключения')
        key_p = 'p1'
        key_P = 'P1'
        var_p1=option_input(*options_p1)

    elif var_p == options[1]:
        key_p = 'p2'
        key_P = 'P2'

    p = parameter_input(key_p)
    P = None
    options_P = ('ввести значение усилия', 'вычислить значение усилия')
    var_P= option_input(*options_P)
    if var_P == options_P[0]:
        P=parameter_input(key_P)
    elif var_P == options_P[1]:
        P = func_P_with_dict(key_P)()
        c[key_P]=P
        w_file()
        P=parameter_input(key_P, message= 'в результате вычисления')

    message_for_d1 = 'В соответствии с заданным усилием при выдвижении ' \
                     'штока {}кН min значение параметра\n'.format(c.get('P1'))

    reference_for_d1 = 'ДЛЯ СПРАВКИ: типовые диаметры(мм) цилиндров(поршня)\n25, ' \
                       '32, 40, 50, 63(65), 80, 100, 125, 140, 160, 180, 200,250, ' \
                       '320, 400\n'
    reference_for_d2 = 'ДЛЯ СПРАВКИ:типовые диаметры штока 12, 14, 18, 22(25), 28' \
                       '(32), 36(40), 45(50), 56, 63, 70, 80, 90, 100, 140, 180, ' \
                       '220 мм\n'
    arg_for_d2 = dict(reference = 'задаём диаметр штока d2 исходя из заданной нагрузки '
                                 '{} (кН) и длины штока {} (мм) по номогррамме.'
                                 '\n'.format(c.get('P1',c.get('P2')),
                                             c.get('L1',c.get('L2'))) + reference_for_d2,
                      image_compiled = image_compiled)

    F = P*100/p   #  определяем требуемую площадь см2(Н/см2==10Bar

    if var_p == options[0] and var_p1 == options_p1[0]:
        d = sqrt(F * 100 / 0.785)
        c['d1'] = d
        w_file()
        d = parameter_input('d1',
                            message= message_for_d1,
                            reference= reference_for_d1
                            )
        parameter_input('d2', **arg_for_d2)

    elif var_p == options[0] and var_p1 == options_p1[1]:
        d = sqrt(F * 100 / 0.785)
        c['d2'] = d
        w_file()
        d = parameter_input('d2',
                            message= 'при дифференциальной схеме рабочей площадью '
                                     'является площадь штока.\n'+ message_for_d1,
                            reference= reference_for_d2)


    elif var_p == options[1]:
        d2 = parameter_input('d2', **arg_for_d2)
        d = sqrt(( F * 100  / 0.786 ) + d2**2)
        msg_for_d2 = 'если диаметр штока определён значением {} мм и\n{} опрелен' \
                     ' значением {}кН, ' \
                     'то min значение'.format(c.get('d2'), messages.get('P2'), c.get('P2'))

        if c.get('P2') < c.get('P1',0) and d < c['d1']:
            d1 = c.get('d1')
            c['d1'] = d
            msg_for_d2 = 'ВНИМАНИЕ:\nтак как {} БОЛЬШЕ чем {}\n ' \
                        'то необходимо учесть ранее заданный d1(мм)- диаметр поршня,' \
                        'равный {}\n\n'.format(messages.get('P1'), messages.get('P2') , d1) + msg_for_d2
        else:
            c['d1'] = d

        parameter_input('d1',
                        message= msg_for_d2,
                        reference= reference_for_d1)
    return 'диаметр поршня d1 = {}\n диаметр штока d2 = {}'.format(c.get('d1'), c.get('d2'))

