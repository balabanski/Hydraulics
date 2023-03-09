# coding=utf-8
from Cylinder.parameters import  file_name
from Cylinder.options import   main_window, font,btn_master, clicked_main_menu, create_img_from_config
from Cylinder.cylinder import *
import tkinter as tk
import json


main_window.title("Расчет параметров цилиндра")


txt_param = tk.Text(main_window, width=50, height=12, font=(font[0], 12))
txt_param.grid(column=0, row=1)

error_open_file_message = '\nне задан файл для хранения параметров\n'

def get_all_param():
    txt_param.delete(0.0,100.100)
    if file_name:
        with open(file_name, 'r') as file:
            c_read = file.read()
        txt_param.insert(0.0, c_read)
    else:
        txt_param.insert(0.0, error_open_file_message)


if file_name:
    txt_param.insert(0.0,'\nпараметры загружены \n для просмотра жми кнопку "параметры"\n')
    main_window.title (file_name)

else:
    txt_param.insert(0.0, error_open_file_message)


btn_all_parameters = tk.Button(main_window, text="Отобразить параметры", font=(font[0], 12),
               command = get_all_param, **btn_master)
btn_all_parameters.grid(column=0, row=0)

def change_param():
    try:
        new_param = txt_param.get(0.0, 100.100)
        _param = json.loads(new_param.replace("'", '"'))
        metadata_cyl.clear()
        for key, val in _param.items():
            metadata_cyl[key ]= val
        w_to_file()#-------------------------------------
        get_all_param()
    except:
        txt_param.delete(0.0, 100.100)
        txt_param.insert(0.0,'ошибка синтаксиса файла json(запятые, двоеточия)\n'
                             'побробуйте еще')



btn_change_parameters = tk.Button(main_window, text="Редактировать & сохранить", font=(font[0], 12),
               command = change_param, **btn_master)
btn_change_parameters.grid(column=1, row=0)



def clicked_selection_d():
    lbl_diameter_selection_d.configure(text=selection_D_and_d())


btn_diameter_selection_d = tk.Button(main_window,
                                     text='подбор диаметра поршня и штока исходя из:'
                                          '\n\t-выбранной конфигурации работы цилиндра \n\t-заданного давления и силы ',
                                     font=(font[0], 12),
                                     command = clicked_selection_d ,
                                     **btn_master)

btn_diameter_selection_d.grid(column=0, row=2)
lbl_diameter_selection_d = tk.Label(main_window, text='результат',
                  font=(font[0], 12))
lbl_diameter_selection_d.grid(column=1, row=2)


lbl_speed_v = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_speed_v.grid(column=1, row=5)
btn_speed_v = tk.Button(main_window, text='v(м/сек) - расчёт фактической скорости',
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_speed_v,
                                              from_config= True,
                                              v1 = v1, v1_diff=v1_diff, v2 = v2),
                  **btn_master)
btn_speed_v.grid(column=0, row=5)

lbl_speed_v_theoretic = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_speed_v_theoretic.grid(column=1, row=6)
btn_speed_v = tk.Button(main_window, text='v(м/сек) - расчёт теоретической скорости',
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_speed_v_theoretic,
                                              from_config= True,
                                              v1_t = v1_t, v1_t_diff = v1_t_diff, v2_t = v2_t),
                  **btn_master)
btn_speed_v.grid(column=0, row=6)


lbl_flow_Q = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_flow_Q.grid(column=1, row=7)
btn_flow_Q = tk.Button(main_window, text='Q(л/мин) - расчёт требуемого(фактического) расхода',
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_flow_Q,
                                              from_config= True,
                                              Q1 = Q1,Q2 = Q2,Q1_diff = Q1_diff),
                  **btn_master)
btn_flow_Q.grid(column=0, row=7)



lbl_force_P = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_force_P.grid(column=1, row=12)
btn_force_P = tk.Button(main_window, text='P(кН) - расчёт требуемого усилия',
                font=(font[0], 12),
                command = clicked_main_menu(lbl_force_P,
                                            from_config= True,
                                            P1= P1, P2 = P2, P1_diff = P1_diff),
                **btn_master)
btn_force_P.grid(column=0, row=12)


lbl_pressure_p = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_pressure_p.grid(column=1, row=17)
btn_pressure_p = tk.Button(main_window, text='p(Bar) -расчет требуемого давления'
                               '(без учета потерь трения)',
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_pressure_p,
                                              from_config= True,
                                              p1= p1,p1_dif = p1_dif, p2 = p2),
                  **btn_master)
btn_pressure_p.grid(column=0, row=17)


lbl_V = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_V.grid(column = 1, row = 19)
btn_V = tk.Button(main_window, text = "V(л.)- вычисление объёма",
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_V,
                                              from_name_par = True,
                                              V1= V1, V1_diff= V1_diff,V2= V2),
                  **btn_master)
btn_V.grid(column=0, row=19)



lbl_area_F = tk.Label(main_window, text='результат', font=(font[0], 12))
lbl_area_F.grid(column=1, row=22)
btn_area_F = tk.Button(main_window, text='F(см2)- расчет площадей',
                  font=(font[0], 12),
                  command = clicked_main_menu(lbl_area_F,
                                              from_name_par = True,
                                              F1= F1, F1_diff= F_diff, F2= F2),
                  **btn_master)
btn_area_F.grid(column=0, row=22)









create_img_from_config()

main_window.mainloop()
