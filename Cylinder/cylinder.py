from math import sqrt
from parameters import c, get_par, parameter_input, w_file, r_file
from debug import *

get_par()# получаю словарь из внешнего фаила или записываю c нулевыми значениями

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
        d= parameter_input(key_d)# ввод параметра и перезапись файла
        if len(args)==0:
            f=F_circle(d)
            return f
        if len(args)==1:
            key_d2 = args[0]
            d2 = parameter_input(key_d2)
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
    v_par= round(v_par,2)
    return v_par


def func_v_with_dict(func_v, key_L, key_t, key_v):
    def _v_with_dict():
        L=c.get(key_L, 0)
        t= parameter_input(key_t)
        if L == 0:
            L = parameter_input(key_L)
        v=func_v(L, t)
        c[key_v] = v
        w_file()
        return v > 0
    return _v_with_dict
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
        v = c.get(key_v,0)
        if v == 0:
            funk_v()
            v = c.get(key_v)
        q=funk_Q(F, v, n_ob = 0.95)
        c[key_q]=q
        w_file()
        return q
    return Q_with_dict
Q1 = func_Q_with_dict(F1,Q, v1, 'v1','Q1') # требуемый расход при выдвижении штока
Q2 = func_Q_with_dict(F2,Q, v2, 'v2','Q2') # требуемый расход при втягивании штока
Q1_diff = func_Q_with_dict(F_diff,Q, v1, 'v1','Q1') # (при дифференциальной схеме)требуемый расход при выдвижении штока




def d():
    '''
    подбор диаметра поршня исходя из заданного давления и силы  (мм)
    диаметр штока d2  ЗАДАЁМ исходя из нагрузги и длины штока по номогррамме для
    определения диаметра штока (стр.439)
    :return: d (мм)
    '''

    var1 =input("выбери схему подключения: \n \t обычная - жми 1 \n \t \
    дифференциальная - жми 2\n")
    if var1=="1":

        var2 =input("выбери вариант приложения нагрузки: \n \t если нажима (при выдвижении \
        штока)-жми 1 \n \t если втягивания - жми 2 \n ")
        if  var2 =="1" :
            p = parameter_input('p1')
            P = P1() # функция для определения требуемого усилия кН
            F = P*100/p   #  определяем требуемую площадь см2(Н/см2==10Bar)
            _d = sqrt(F * 100 / 0.785)
            print ("min диаметр поршня при  нажиме равен:  - ", _d)
        if var2=="2" :
            p = parameter_input('p2')
            P = P2() # функция для определения требуемого усилия кН
            d2 = float(input('задаём диаметр штока d2 исходя из нагрузки {} и длины штока по \
            номогррамме. \nОсновные размеры:15, 16, 18, 20, 25, 32, 40, 50, 63, 80, 100 мм\n'.format(c.get('P1', 0))))
            _d  =sqrt(( F * 100  / 0.786 ) + d2**2)
            print ('если диаметр штока определён значением {} мм , то \
            min диаметр поршня при втягивании равен:  - {} мм'.format(d2, _d))
        c['d1'] = _d
    if var1 == "2":
        print('при дифференциальной схеме полезной площадью является площадь штока\n\
        исходя из этого минимальный диаметр штока :')
        p = parameter_input('p1')
        P = P1() # функция для определения требуемого усилия кН
        F = P*100/p   #  определяем требуемую площадь см2(Н/см2==10Bar)
        _d = sqrt(F * 100 / 0.785)#  min диаметр штока
        c['d2'] = _d
    w_file()
    return _d




# сила (кН)   (m = тн, а=м/с2)
def P(m, a, g=9.8):
    _P= a * m + (g * m)
    return _P             # кН


# функция для вычисления требуемого усилия
def func_P_with_dict(key_P):
    def _P_with_dict():
        m = parameter_input('m')        
        var=input("если хочешь получить  значение требуемого усилия исходя из приведенной \
        массы(при подъёме) -жми 1 \nесли исходя из ускорения (при горизонтальном перемещении)- жми 2 \n")
        if var== '1':
            try:
                 _a=float(input("ускорение по умолчанию 0 м/с2 , введи другое значение или жми \
                    кнопку 'ввод'\n"))
                 _P=P(m ,_a )
            except:
                 _P=P(m )
        if var == '2':
            a=float(input('введи значение ускорения (м/сек2)  '))
            _P=P(m, a, g=0)
        c[key_P] = round(_P, 2)
        w_file()
        return _P
    return _P_with_dict
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
        var_P= input('что бы ВВЕСТИ значение  усилия (кН)- жми 1\n\
        если хочешь ВЫЧИСЛИТЬ значение  усилия - жми 2\n ')
        if var_P == "1":
           _P = parameter_input(key_P)
        if var_P == "2":
            _P = func_P()
        _p = p(_P, F)
        c[key_p] = _p
        w_file()
        return _p
    return _p_with_dict
p1 = func_p_with_dict(F1,P1,'p1', 'P1') # требуемое давление при выдвижении штока
p2 = func_p_with_dict(F2,P2,'p2', 'P2') # требуемое давление при втягивании штока
