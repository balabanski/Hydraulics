# coding=utf-8
from Cylinder.parameters import file_id
from utils.parameters import font,btn_master
from Cylinder.options import main_window_cyl, clicked_main_menu_cyl, create_img_from_config
from Cylinder.cylinder import metadata, selection_D_and_d,\
    v1, v1_diff, v2, Q1, Q2, Q1_diff, P1, P2, P1_diff, p1, p2, p1_dif, V1_diff, V1, V2, F_diff, F1, F2,\
    v1_fact, v1_diff_f, v2_fact, t1, t2, t1_diff

import tkinter as tk
import asyncio
from src.schemas import IFileUpdateSchema
from src.repositories.file import update_file

from utils._app import get_all_parameters



main_window_cyl.title("Расчет параметров цилиндра")

get_all_parameters_cyl= get_all_parameters(main_window = main_window_cyl,
                                           file_name = file_id,
                                           metadata = metadata,
                                           )

get_all_parameters_cyl()


# подбор диаметра поршня и штока исходя из:------------------------------------
#    -выбранной конфигурации работы цилиндра
#    -заданного давления и силы
def clicked_selection_d():
    lbl_diameter_selection_d.configure(text=selection_D_and_d())
    asyncio.run(update_file(file_id=file_id, file=IFileUpdateSchema(meta_data=metadata)))


btn_diameter_selection_d = tk.Button(main_window_cyl,
                                     text='подбор диаметра поршня и штока исходя из:'
                                          '\n\t-выбранной конфигурации работы цилиндра \n\t-заданного давления и силы ',
                                     font=(font[0], 12),
                                     command = clicked_selection_d ,
                                     **btn_master)

btn_diameter_selection_d.grid(column=0, row=2)
lbl_diameter_selection_d = tk.Label(main_window_cyl, text='результат',
                  font=(font[0], 12))
lbl_diameter_selection_d.grid(column=1, row=2)


#  - расчёт теоретической скорости---------------------------------------------
lbl_speed_v_theoretic = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_speed_v_theoretic.grid(column=1, row=6)
btn_speed_v = tk.Button(main_window_cyl, text='v(м/сек) - расчёт теоретической скорости',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_speed_v_theoretic,
                                              from_config= True,
                                              message= True,
                                              v1 = v1, v1_diff = v1_diff, v2 = v2),
                  **btn_master)
btn_speed_v.grid(column=0, row=6)

# - расчёт требуемого(фактического) расхода----------------------------
lbl_flow_Q = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_flow_Q.grid(column=1, row=7)
btn_flow_Q = tk.Button(main_window_cyl, text='Q(л/мин) - расчёт требуемого(фактического) расхода',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_flow_Q,
                                              from_config= True,
                                              message= True,
                                              Q1 = Q1,Q2 = Q2,Q1_diff = Q1_diff),
                  **btn_master)
btn_flow_Q.grid(column=0, row=7)


# - расчёт требуемого усилия------------------------------------------
lbl_force_P = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_force_P.grid(column=1, row=12)
btn_force_P = tk.Button(main_window_cyl, text='P(кН) - расчёт требуемого усилия',
                font=(font[0], 12),
                command = clicked_main_menu_cyl(lbl_force_P,
                                            from_config= True,
                                            message= True,
                                            P1= P1, P2 = P2, P1_diff = P1_diff),
                **btn_master)
btn_force_P.grid(column=0, row=12)


# -расчет требуемого давления--------------------------------------------
lbl_pressure_p = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_pressure_p.grid(column=1, row=17)
btn_pressure_p = tk.Button(main_window_cyl, text='p(Bar) -расчет требуемого давления'
                               '(без учета потерь трения)',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_pressure_p,
                                              from_config= True,
                                              message= True,
                                              p1= p1,p1_dif = p1_dif, p2 = p2),
                  **btn_master)
btn_pressure_p.grid(column=0, row=17)


# -расчетное время хода поршня--------------------------------------------
lbl_time_t = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_time_t.grid(column=1, row=18)
btn_time_t = tk.Button(main_window_cyl, text='t(сек.) -расчетное время хода поршня',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_time_t,
                                              from_config= True,
                                              message= True,
                                              t1= t1, t1_diff = t1_diff, t2 = t2),
                  **btn_master)
btn_time_t.grid(column=0, row=18)




# - вычисление объёма---------------------------------------------------
lbl_V = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_V.grid(column = 1, row = 19)
btn_V = tk.Button(main_window_cyl, text = "V(л.)- вычисление объёма",
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_V,
                                              from_name_par = True,
                                              V1= V1, V1_diff= V1_diff,V2= V2),
                  **btn_master)
btn_V.grid(column=0, row=19)


# - расчет площадей--------------------------------------------------
lbl_area_F = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_area_F.grid(column=1, row=22)
btn_area_F = tk.Button(main_window_cyl, text='F(см2)- расчет площадей',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_area_F,
                                              from_name_par = True,
                                              F1= F1, F1_diff= F_diff, F2= F2),
                  **btn_master)
btn_area_F.grid(column=0, row=22)


# - расчёт фактической скорости-----------------------------------------------
lbl_speed_v = tk.Label(main_window_cyl, text='результат', font=(font[0], 12))
lbl_speed_v.grid(column=1, row=24)
btn_speed_v = tk.Button(main_window_cyl, text='фактические t(время)-v(скорость) хода поршня\n'
                                              'и расчетная подача Q',
                  font=(font[0], 12),
                  command = clicked_main_menu_cyl(lbl_speed_v,
                                              from_config= True,
                                              message= True,
                                              v1_fact = v1_fact, v1_diff_f=v1_diff_f, v2_fact = v2_fact),
                  **btn_master)
btn_speed_v.grid(column=0, row=24)


create_img_from_config()

main_window_cyl.mainloop()
