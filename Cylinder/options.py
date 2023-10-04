import tkinter as tk
from pathlib import Path
from Cylinder.parameters import metadata, name_par_cyl, file_id
from utils.options import insert_image, option_input, clicked_main_menu

main_window_cyl = tk.Tk()

direction = ('выдвижение штока (давление в поршневой полости)', 'втягивание штока (давление в штоковой полости)')
dif_or_no = ('обычная схема подключения(штоковая и поршневая полости разделены)',
             'выдвижение штока(дифференциальная схема подлючения)')
arrangement = (
'горизонтальное расположение цилиндра', 'вертикальное расположение цилиндра\n либо расчет исходя из приведённой массы')

config_cyl = {
    "v1": direction[0],
    "v2": direction[1],
    "v1_diff": dif_or_no[1],
    'v1_fact': direction[0],
    'v1_diff_f': dif_or_no[1],
    'v2_fact': direction[1],
    "p1": direction[0],
    "p2": direction[1],
    "p1_dif": dif_or_no[1],
    "Q1": direction[0],
    "Q2": direction[1],
    "Q1_diff": dif_or_no[1],
    "P1": direction[0],
    "P2": direction[1],
    "P1_diff": dif_or_no[1],
    "t1": direction[0],
    "t2": direction[1],
    "t1_diff": dif_or_no[1],
}

dir_images_for_cyl = str(Path(Path.cwd(), 'Cylinder', 'images'))

out_gor_1 = insert_image(dir_images_for_cyl + '//zylhordausP.gif')
dif_gor_1 = insert_image(dir_images_for_cyl + '//dif_ zylhordausP.gif')
dif_ver_1 = insert_image(dir_images_for_cyl + '//dif_ ver_zylhordausP.gif')
in_gor_1 = insert_image(dir_images_for_cyl + '//zylhordeinM.gif')
gor_2 = insert_image(dir_images_for_cyl + '//zylhorgausP.gif')
ver_1_p1 = insert_image(dir_images_for_cyl + '//zyl_Verdaus_p1.gif')
ver_1_p2 = insert_image(dir_images_for_cyl + '//zyl_Verhdein_p2.gif')


def create_img_from_config():
    if metadata.get('config') is not None:
        if metadata.get('config').get('direction') == 'p1':
            if metadata.get('config').get('arrangement') == "vertical movement":
                ver_1_p1(main_window_cyl).grid(row=1, column=1)
            else:
                out_gor_1(main_window_cyl).grid(row=1, column=1)

        elif metadata.get('config').get('direction') == 'p1_diff':
            if metadata.get('config').get('arrangement') == "vertical movement":
                dif_ver_1(main_window_cyl).grid(row=1, column=1)
            else:
                dif_gor_1(main_window_cyl).grid(row=1, column=1)

        elif metadata.get('config').get('direction') == 'p2':
            if metadata.get('config').get('arrangement') == "vertical movement":
                ver_1_p2(main_window_cyl).grid(row=1, column=1)
            else:
                in_gor_1(main_window_cyl).grid(row=1, column=1)


def _img_from_type_cyl(window_, type_):
    if metadata.get('config') is None:        
        metadata['config'] = {}

    if type_.get() == direction[0]:
        out_gor_1(window_).grid(row=4, column=0)  # , column = 0, columnspan= 1)
        dif_gor_1(window_).grid(row=4, column=1)
        metadata['config']['direction'] = 'p1'

    elif type_.get() == direction[1]:
        in_gor_1(window_).grid(row=4, column=0)
        gor_2(window_).grid(row=4, column=1)
        metadata['config']['direction'] = 'p2'

    if type_.get() == dif_or_no[0]:
        out_gor_1(window_).grid(row=4, column=0)

    elif type_.get() == dif_or_no[1]:
        dif_gor_1(window_).grid(row=4, column=0)
        metadata['config']['direction'] = 'p1_diff'

    if type_.get() == arrangement[0]:
        metadata['config']['arrangement'] = "horizontal movement"

        if metadata.get('config').get('direction') == 'p1':
            out_gor_1(window_).grid(row=4, column=0)

        elif metadata.get('config').get('direction') == 'p1_diff':
            dif_gor_1(window_).grid(row=4, column=0)

        elif metadata.get('config').get('direction') == 'p2':
            in_gor_1(window_).grid(row=4, column=0)

    elif type_.get() == arrangement[1]:
        metadata['config']['arrangement'] = "vertical movement"

        if metadata.get('config').get('direction') == 'p1':
            ver_1_p1(window_).grid(row=4, column=0)

        elif metadata.get('config').get('direction') == 'p1_diff':
            dif_ver_1(window_).grid(row=4, column=0)

        elif metadata.get('config').get('direction') == 'p2':
            ver_1_p2(window_).grid(row=4, column=0)


def set_type_from_config(type_):
    if metadata['config']['direction'] == 'p1':
        type_.set(direction[0])
    elif metadata['config']['direction'] == 'p1_diff':
        type_.set(dif_or_no[1])
    elif metadata['config']['direction'] == 'p2':
        type_.set(direction[1])


# экземпляр функции option_input (for cylinder)
option_input_cyl = option_input(func_img_from_type=_img_from_type_cyl,
                                func_create_img_from_config=create_img_from_config,
                                func_set_type_from_config=set_type_from_config,
                                config_json=config_cyl,
                                name_par_json=name_par_cyl,
                                )

# экземпляр функции clicked_main_menu (for cylinder)
clicked_main_menu_cyl = clicked_main_menu(metadata=metadata,
                                          funk_option_input=option_input_cyl,
                                          file_name=file_id,
                                          config_json=config_cyl)
