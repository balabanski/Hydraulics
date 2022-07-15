# coding=utf-8
from Cylinder.cylinder import *
from Cylinder.parameters import  messages, file_name
import tkinter as tk



font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')


window = tk.Tk()
window.title("Расчет параметров цилиндра")


txt_param = tk.Text(width=30, height=12, font=(font[0], 12))
txt_param.grid(column=1, row=0)


def get_all_param():
    # file_name = fd.askopenfilename()
    with open(file_name, 'r') as file:
        c_read = file.read()
    txt_param.insert(1.0, c_read)

btn_all_parameters = tk.Button(text="Все параметры", font=(font[0], 12),
               command = get_all_param, **btn_master)
btn_all_parameters.grid(column=0, row=0)




def click_F1():
    par = F1()
    lbl_area_F1.configure(text = par)
    lbl_area_F2.configure(text = F_ring(c.get('d1',0), c.get('d2',0)))

btn_area_F1 = tk.Button(window, text='{}'.format(messages['F1']),
                  font=(font[0], 12), command = click_F1, **btn_master)
btn_area_F1.grid(column=0, row=1)

lbl_area_F1 = tk.Label(window, text='результат', font=(font[0], 12))
lbl_area_F1.grid(column=1, row=1)



def click_F2():
    par = F2()
    lbl_area_F2.configure(text = par)
    lbl_area_F1.configure(text = F_circle(c.get('d1',0)))

btn_area_F2 = tk.Button(window, text='{}'.format(messages['F2']),
                  font=(font[0], 12), command = click_F2, **btn_master)
btn_area_F2.grid(column=0, row=2)

lbl_area_F2 = tk.Label(window, text='результат', font=(font[0], 12))
lbl_area_F2.grid(column=1, row=2)



lbl_speed_v = tk.Label(window, text='результат', font=(font[0], 12))
lbl_speed_v.grid(column=1, row=3)
btn_speed_v = tk.Button(window, text='v(м/сек) - расчёт фактической скорости',
                  font=(font[0], 12),
                  command = clicked_main_menu(3,lbl_speed_v,v1 = v1, v2 = v2),
                  **btn_master)
btn_speed_v.grid(column=0, row=3)



lbl_flow_Q = tk.Label(window, text='результат', font=(font[0], 12))
lbl_flow_Q.grid(column=1, row=7)
btn_flow_Q = tk.Button(window, text='Q(л/мин) - расчёт требуемого(фактического) расхода',
                  font=(font[0], 12),
                  command = clicked_main_menu(7,lbl_flow_Q, Q1 = Q1,Q2 = Q2,Q1_diff = Q1_diff),
                  **btn_master)
btn_flow_Q.grid(column=0, row=7)



lbl_force_P = tk.Label(window, text='результат', font=(font[0], 12))
lbl_force_P.grid(column=1, row=12)
btn_force_P = tk.Button(window, text='P(кН) - расчёт требуемого усилия',
                font=(font[0], 12),
                command = clicked_main_menu(13,lbl_force_P,
                                            P1= P1, P2 = P2),
                **btn_master)
btn_force_P.grid(column=0, row=12)


lbl_pressure_p = tk.Label(window, text='результат', font=(font[0], 12))
lbl_pressure_p.grid(column=1, row=17)
btn_pressure_p = tk.Button(window, text='вычисление требуемого давления'
                               '(без учета потерь трения)',
                  font=(font[0], 12),
                  command = clicked_main_menu(17,lbl_pressure_p,
                                              p1= p1, p2 = p2),
                  **btn_master)
btn_pressure_p.grid(column=0, row=17)



btn_diameter_selection_d = tk.Button(window, text='подбор диаметра поршня (и штока)исходя из заданного давления и силы \n'
                                                  '(пока не работает в окне приложения)',
                   font=(font[0], 15), **btn_master)
btn_diameter_selection_d.grid(column=0, row=40)
lbl_diameter_selection_d = tk.Label(window, text='результат',
                  font=(font[0], 15))
lbl_diameter_selection_d.grid(column=1, row=40)


def clicked_selection_d():
    lbl_diameter_selection_d.configure(text=d())


btn_diameter_selection_d['command'] = clicked_selection_d

window.mainloop()
