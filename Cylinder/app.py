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


lbl_F1 = tk.Label(window, text='результат', font=(font[0], 15))
lbl_F1.grid(column=1, row=1)

def clicked_F1():
    command_for_F1()

btn_F1 = tk.Button(window, text='{}'.format(messages['F1']),
                  font=(font[0], 15), command = clicked_F1, **btn_master)
btn_F1.grid(column=0, row=1)



lbl_F2 = tk.Label(window, text='результат', font=(font[0], 15))
lbl_F2.grid(column=1, row=2)

def clicked_F2():
    command_for_F2()

btn_F2 = tk.Button(window, text='{}'.format(messages['F2']),
                  font=(font[0], 15), command = clicked_F2, **btn_master)
btn_F2.grid(column=0, row=2)

def clicked_(lbl1, lbl2, func1, func2):
        def clicked__():
            try:
                par = float(ent.get())
                c[key] = par
                w_file()  # перезаписываю файл
                return par
            except:
                par = c.get(key, 0)
                return par
            finally:
                lbl1.configure(text=func1())
                lbl2.configure(text=func2())
        return clicked__
_F1 = clicked_(lbl_F1, lbl_F2, F1, F2)
_F2 = clicked_(lbl_F2, lbl_F1, F2, F1)





def parameter_input(func_command, *keys):
        def _parameter_input():
            global key
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
                                command=func_command,
                                font=(font[0], 15))
                btn.grid(column=0, row=1)

                window_.grab_set()
                window_.wait_window() #запускает локальный цикл событий, который завершается после уничтожения окна
        return _parameter_input
command_for_F1 = parameter_input(_F1, 'd1')
command_for_F2 = parameter_input(_F2, 'd1', 'd2')


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
