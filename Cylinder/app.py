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
    parameter_input('d1')

def parameter_input(key):
    title_text = "ввод параметра {}".format(messages.get(key))
    window_ = tk.Tk()
    window_.title(title_text)


    lbl_text = 'параметр {} определён значением {}'.format(messages.get(key), c.get(key, 0))+\
               '\n (можешь ввести новое значение в поле справа'+\
               '\n либо ничего не вводить и оставить прежним)'

    lbl = tk.Label(window_, text= lbl_text,
              font=(font[0], 15),
              **btn_master)
    lbl.grid(column = 0, row = 0)

    def clicked_d():
        try:
            par = float(ent.get())
            c[key] = par
            w_file() #перезаписываю файл
            return par
        except:
            par = c.get(key, 0)
            return par
        finally:
            lbl_F1.configure(text = F1())
            lbl_F2.configure(text = F2())






    ent = tk.Entry(window_,  font=(font[0], 15))
    ent.grid(column = 1, row = 0)

    btn = tk.Button(window_, text=' подтвердить запись',
                    command = clicked_d,
                    font=(font[0], 15))
    btn.grid(column = 0, row = 1)



    window_.mainloop()


'''
def clicked_F1():
    key = 'd1'
    title_text = "Расчет площади поршня"
    window_ = tk.Tk()
    window_.title(title_text)
    par = c.get(key, 0)

    lbl_text = 'параметр {} определён значением {}'.format(messages.get(key), par)+\
               '\n (можешь ввести новое значение в поле справа)'

    def clicked_d(f_d = F_ring):
        try:
            c[key] = float(ent.get())
            w_file() #перезаписываю файл
            lbl_F2.configure(text = f_d(c[key],c['d2']))
        except:
            pass
        lbl_1.configure(text=F_circle(c[key]))

    lbl = tk.Label(window_, text= lbl_text,
              font=(font[0], 15),
              **btn_master).grid(column = 0, row = 0)

    ent = tk.Entry(window_,  font=(font[0], 15))
    ent.grid(column = 1, row = 0)

    btn = tk.Button(window_, text='расчет',
                    command = clicked_d,
                    font=(font[0], 15))
    btn.grid(column = 0, row = 1)

    window_.mainloop()
'''





btn_F1 = tk.Button(window, text='{}'.format(messages['F1']),
                  font=(font[0], 15), **btn_master)
btn_F1.grid(column=0, row=1)

btn_F1['command'] = clicked_F1

btn_F2 = tk.Button(window, text='{}'.format(messages['F2']),
                  font=(font[0], 15), **btn_master)
btn_F2.grid(column=0, row=2)
lbl_F2 = tk.Label(window, text='результат', font=(font[0], 15))
lbl_F2.grid(column=1, row=2)


def clicked_2():
    lbl_F2.configure(text=F2())
    lbl_F1.configure(text=F_circle(c['d1']))


btn_F2['command'] = clicked_2

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
