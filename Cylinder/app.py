# coding=utf-8
from Cylinder.cylinder import *
from Cylinder.parameters import c, messages, file_name
import tkinter as tk


font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')


window = tk.Tk()
window.title("Расчет параметров цилиндра")


txt_param = tk.Text(width=30, height=12, font=(font[0], 15))
txt_param.grid(column=1, row=0)


def get_param():
    # file_name = fd.askopenfilename()
    with open(file_name, 'r') as file:
        c_read = file.read()
    txt_param.insert(1.0, c_read)


b1 = tk.Button(text="Все параметры", font=(font[0], 13),
               command = get_param, **btn_master)
b1.grid(column=0, row=0)




def click_F1():
    par = F1()
    lbl_F1.configure(text = par)
    lbl_F2.configure(text = F_ring(c.get('d1',0), c.get('d2',0)))

btn_F1 = tk.Button(window, text='{}'.format(messages['F1']),
                  font=(font[0], 15), command = click_F1, **btn_master)
btn_F1.grid(column=0, row=1)

lbl_F1 = tk.Label(window, text='результат', font=(font[0], 15))
lbl_F1.grid(column=1, row=1)



def click_F2():
    par = F2()
    lbl_F2.configure(text = par)
    lbl_F1.configure(text = F_circle(c.get('d1',0)))

btn_F2 = tk.Button(window, text='{}'.format(messages['F2']),
                  font=(font[0], 15), command = click_F2, **btn_master)
btn_F2.grid(column=0, row=2)

lbl_F2 = tk.Label(window, text='результат', font=(font[0], 15))
lbl_F2.grid(column=1, row=2)


def clicked_main(row_,func1,func2, *keys):
    """
    функция фабрики закрытия для кнопок основного окна и выбора вариантов
    """
    def clicked_():
        global row
        row = row_
        _types = ['{}'.format(messages[key]) for key in keys]
        print(_types)
        _type = tk.StringVar()
        _type.set(_types[0])
        radios = [tk.Radiobutton(text=t, value=t, variable=_type,font=(font[0], 15)) for t in _types]
        for radio in radios:
            row = row+1
            radio.grid(column=0, row = row)

        def click():
            par = None
            if _type.get() == _types[0]:
                par = func1()
            if _type.get() == _types[1]:
                par = func2()
            lbl_v.configure(text = par)

        btn = tk.Button(window, text='подтвердить выбор',
                      font=(font[0], 15), command = click, **btn_master)
        btn.grid(column=0, row = row+1)
        print(row)
    return clicked_


btn_v = tk.Button(window, text='Расчёт фактической скорости(м/сек)',
                  font=(font[0], 15), command = clicked_main(3,v1,v2,'v1','v2'), **btn_master)
btn_v.grid(column=0, row=3)
lbl_v = tk.Label(window, text='результат', font=(font[0], 15))
lbl_v.grid(column=1, row=3)


btn_12 = tk.Button(window, text='подбор диаметра поршня (и штока)исходя из заданного давления и силы',
                   font=(font[0], 15), **btn_master)
btn_12.grid(column=0, row=9)
lbl_12 = tk.Label(window, text='результат',
                  font=(font[0], 15))
lbl_12.grid(column=1, row=9)


def clicked_12():
    lbl_12.configure(text=d())


btn_12['command'] = clicked_12

window.mainloop()
