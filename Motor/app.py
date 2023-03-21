from Motor.parameters import file_name_mot, w_to_file_mot, metadata_mot
from Motor.motor import V, n, Q, p, M, P
import tkinter as tk
from utils.parameters import font, btn_master
from utils._app import get_all_parameters


main_window_mot = tk.Tk()
main_window_mot.title('расчет параметров гидромотора')

get_all_parameters_mot= get_all_parameters(main_window = main_window_mot,
                                           file_name = file_name_mot,
                                           metadata = metadata_mot,
                                           func_w_to_file = w_to_file_mot,)

get_all_parameters_mot()


def click_main_menu(label, func):
    def _click_main_menu():
        label.configure(text = func())
        w_to_file_mot()
    return _click_main_menu


# расчёт рабочего объёма---------------------------------------------
lbl_V = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_V.grid(column=1, row=6)
btn_V = tk.Button(main_window_mot, text='V(см3) - расчёт рабочего объёма',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_V, V),
                  **btn_master)
btn_V.grid(column=0, row=6)


# расчёт скорости вращения n(об/мин)--------------------------------
lbl_n = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_n.grid(column=1, row=8)
btn_n = tk.Button(main_window_mot, text='n(об/мин) - расчёт скорости вращения',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_n, n),
                  **btn_master)
btn_n.grid(column=0, row=8)


# расчёт требуемой подачи Q(л/мин)--------------------------------
lbl_Q = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_Q.grid(column=1, row=9)
btn_Q = tk.Button(main_window_mot, text='Q(л/мин) - расчёт требуемой подачи',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_Q, Q),
                  **btn_master)
btn_Q.grid(column=0, row=9)


# расчёт требуемого давления(перепад давления) p(Bar)------------------
lbl_p = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_p.grid(column=1, row=10)
btn_p = tk.Button(main_window_mot, text='p(Bar) - расчет требуемого давления(перепад давления)',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_p, p),
                  **btn_master)
btn_p.grid(column=0, row=10)


# расчёт вращающего момента ведомого вала M(даН*м)---------------------
lbl_M = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_M.grid(column=1, row=11)
btn_M = tk.Button(main_window_mot, text='M(даН*м) - расчёт вращающего момента ведомого вала',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_M, M),
                  **btn_master)
btn_M.grid(column=0, row=11)


# расчёт мощности ведомого вала P(кВт)---------------------
lbl_P = tk.Label(main_window_mot, text='результат', font=(font[0], 12))
lbl_P.grid(column=1, row=13)
btn_P = tk.Button(main_window_mot, text='P(кВт) - расчёт мощности ведомого вала',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_P, P),
                  **btn_master)
btn_P.grid(column=0, row=13)


main_window_mot.mainloop()
