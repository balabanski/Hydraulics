import json
import tkinter as tk
from types import FunctionType
from pathlib import Path


font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')

c = {}

messages = {
    "F1": 'F1 (см2) -площадь поршня ',
    "F2": 'F2 (см2) -пплощадь кольцевого сечения',
    "d1": 'd1 (мм)-диаметр поршня ',
    "d2": 'd2 (мм)-диаметр штока ',
    "t1": 't1 (сек)-время выдвижения штока',
    "t2": 't2 (сек)-время втягивания штока',
    "v1": "v1 (м/сек)скорость при выдвижении штока ",
    "v2": "v2 (м/сек)скорость при втягивании штока ",
    "Q1": "Q1 (л/мин)- требуемая подача в поршневую полость",
    "Q2": "Q2 (л/мин)- требуемая подача в штоковую полость",
    "Q1_diff": "Q1_diff (л/мин)- (при дифференциальной схеме)требуемая подача при выдвижении штока",
    "P1": 'P1 (кН) - усилие при выдвижении штока',
    "P2": 'P2 (кН) - усилие при втягивании штока',
    "m": 'm (тн) - масса груза',
    "p1": 'p1 (Bar) - давление в поршневой полости',
    "p2": 'p2 (Bar) - давление в штоковой полости',
    "L1": 'L 1(мм)- ход поршня при выдвижении штока ',
    "L2": 'L 2(мм)- ход поршня при втягивании штока ',
}

# файлы для записи и чтения

# file_name = "E:/ГИДРООБОРУДОВАНИЕ/7535  Кран  'PRESTEL'/УСКОРЯЮ PRESTEL/7535_PRESTEL.json"
file_name = 'C:/Python34/MyLessons/Hydraulics/Cylinder/JsonFiles/cylinder.json'
#file_name = str(Path(Path.cwd(),'Cylinder','JsonFiles', 'cylinder.json'))# работает только с main.py

#  запись
def w_file():
    with open(file_name, 'w')as file:
        json.dump(c, file, sort_keys=True, indent=4)


# чтение   
def r_file():
    with open(file_name, 'r') as file:
        c_read = json.load(file)
    for key, val in c_read.items():
        c[key] = val
        if c[key] != 0:
            print('    {}:{:>2}'.format(key, val))


# получаю словарь из внешнего фаила или записываю
def get_par():
    try:
        r_file()
    except:
        print("запись имеющихся  значений в файл {}".format(file_name))
        w_file()


# ввод запрашиваемых значений и перезапись файла
def parameter_input(*keys):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """
    def clicked():
        try:
            par = float(ent.get())
            c[key] = par
            w_file()  # перезаписываю файл
        except:
            par = c.get(key, 0)
        btn.configure(text='закрыть для продолжения и получения результатов',
                    command=window_.destroy)
        return par

    for key in keys:
        window_ = tk.Toplevel()
        global ent
        title_text = "ввод параметра {}".format(messages.get(key))

        window_.title(title_text)
        lbl_text = 'параметр {} определён значением {}'.format(messages.get(key), c.get(key, 0)) + \
                   '\n (можешь ввести новое значение в поле справа' + \
                   '\n либо ничего не вводить и оставить прежним)'
        lbl = tk.Label(window_, text=lbl_text,
                       font=(font[0], 15),
                       **btn_master)
        lbl.grid(column=0, row=0)

        ent = tk.Entry(window_, font=(font[0], 15))
        ent.grid(column=1, row=0)
        btn = tk.Button(window_, text=' подтвердить запись',
                        command=clicked,
                        font=(font[0], 15))
        btn.grid(column=0, row=1)

        window_.grab_set()
        window_.wait_window()  #запускает локальный цикл событий, который
        # завершается после уничтожения окна


def clicked_main_menu(row_,lbl_result,**kwargs):
    """
    функция фабрики закрытия - расширяем текущее окно дополнительными виджетами
    -для возможности выбора вариантов исполнения чего-либо
    -для вычисления и вывода полученного результата
    :)
    """
    def clicked_():
        row = row_
        _types = [messages[key] for key, funk in sorted(kwargs.items())]
        _type = tk.StringVar()
        _type.set(_types[0])
        radios = [tk.Radiobutton(text=t, value=t, variable=_type,font=(font[0], 15)) for t in _types]
        for radio in radios:
            row = row+1
            radio.grid(column=0, row = row)

        def click():
            for key, funk in kwargs.items():
                if _type.get() == messages[key] :
                    if type(funk) is FunctionType:
                        par = funk()
                        lbl_result.configure(text = par)
                    else:
                        lbl_result.configure(text = 'это не фунция')

        btn = tk.Button(text='подтвердить выбор',font=(font[0], 15),
                        command = click, **btn_master)
        btn.grid(column=0, row = row+1)
        print(row)
    return clicked_


'''
#запись
def w_file(file='cilinder.txt'):
    with open(file, 'w')as file:
        for key,val in cil.items():
            file.write('{}:{} \n'.format(key, str(val)))
    pass

#чтение
def r_file(file='cilinder.txt'):
    new={}
    with open(file, 'r')as file:
        for i in file.readlines():
            key,val = i.strip().split(':')
            new[key]=val
    print (new) 
'''


