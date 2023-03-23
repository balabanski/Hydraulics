from Pump.parameters import file_name_pump, w_to_file_pump, metadata_pump, r_from_file_pump
from Pump.pump import V, Q, P
import tkinter as tk
from utils.parameters import font, btn_master
from utils._app import get_all_parameters



main_window_pump = tk.Tk()
main_window_pump.title('расчет параметров гидронасоса')

get_all_parameters_pump= get_all_parameters(main_window = main_window_pump,
                                           file_name = file_name_pump,
                                           metadata = metadata_pump,
                                           func_w_to_file = w_to_file_pump,
                                           func_read_from_file_to_metadata= r_from_file_pump,
                                           )

get_all_parameters_pump()


def click_main_menu(label, func):
    def _click_main_menu():
        label.configure(text = func())
        w_to_file_pump()
    return _click_main_menu

# расчёт рабочего объёма---------------------------------------------
lbl_V = tk.Label(main_window_pump, text='результат', font=(font[0], 12))
lbl_V.grid(column=1, row=6)
btn_V = tk.Button(main_window_pump, text='V(см3) - расчёт рабочего объёма',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_V, V),
                  **btn_master)
btn_V.grid(column=0, row=6)


# расчёт требуемой подачи Q(л/мин)--------------------------------
lbl_Q = tk.Label(main_window_pump, text='результат', font=(font[0], 12))
lbl_Q.grid(column=1, row=9)
btn_Q = tk.Button(main_window_pump, text='Q(л/мин) - расчёт требуемой подачи',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_Q, Q),
                  **btn_master)
btn_Q.grid(column=0, row=9)


# расчёт мощности привода насоса P(кВт)---------------------
lbl_P = tk.Label(main_window_pump, text='результат', font=(font[0], 12))
lbl_P.grid(column=1, row=13)
btn_P = tk.Button(main_window_pump, text='P(кВт) - расчёт мощности ведомого вала',
                  font=(font[0], 12),
                  command = click_main_menu(lbl_P, P),
                  **btn_master)
btn_P.grid(column=0, row=13)


main_window_pump.mainloop()