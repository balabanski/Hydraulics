from Motor.parameters import file_name_mot, w_to_file_mot, metadata_mot
from Motor.motor import V, n, Q, p, M, P
import tkinter as tk
import json
from utils.parameters import font, btn_master



main_window_mot = tk.Tk()
main_window_mot.title('расчет параметров гидромотора')

txt_param = tk.Text(main_window_mot, width=50, height=12, font=(font[0], 12))
txt_param.grid(column=0, row=1)

error_open_file_message = '\nне задан файл для хранения параметров\n'

def get_all_param():
    txt_param.delete(0.0,100.100)
    if file_name_mot:
        with open(file_name_mot, 'r') as file:
            c_read = file.read()
        txt_param.insert(0.0, c_read)
    else:
        txt_param.insert(0.0, error_open_file_message)


if file_name_mot:
    txt_param.insert(0.0,'\nпараметры загружены \n для просмотра жми кнопку "параметры"\n')
    main_window_mot.title (file_name_mot)

else:
    txt_param.insert(0.0, error_open_file_message)


btn_all_parameters = tk.Button(main_window_mot, text="Отобразить параметры", font=(font[0], 12),
               command = get_all_param, **btn_master)
btn_all_parameters.grid(column=0, row=0)

def change_param():
    try:
        new_param = txt_param.get(0.0, 100.100)
        _param = json.loads(new_param.replace("'", '"'))
        metadata_mot.clear()
        for key, val in _param.items():
            metadata_mot[key ]= val
        w_to_file_mot()
        get_all_param()
    except:
        txt_param.delete(0.0, 100.100)
        txt_param.insert(0.0,'ошибка синтаксиса файла json(запятые, двоеточия)\n'
                             'побробуйте еще')

btn_change_parameters = tk.Button(main_window_mot, text="Редактировать & сохранить", font=(font[0], 12),
               command = change_param, **btn_master)
btn_change_parameters.grid(column=1, row=0)



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
