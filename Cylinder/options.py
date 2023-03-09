import tkinter as tk
from types import FunctionType
from pathlib import Path
from Cylinder.parameters import metadata_cyl,  btn_master, font, name_par,w_to_file

main_window = tk.Tk()

direction = ('выдвижение штока (давление в поршневой полости)', 'втягивание штока (давление в штоковой полости)')
dif_or_no = ('обычная схема подключения(штоковая и поршневая полости разделены)',
             'выдвижение штока(дифференциальная схема подлючения)')
arrangement = ( 'горизонтальное расположение цилиндра', 'вертикальное расположение цилиндра\n либо расчет исходя из приведённой массы')

config = {
    "v1": direction[0],
    "v2": direction[1],
    "v1_diff": dif_or_no[1],
    'v1_t': direction[0],
    'v1_t_diff': dif_or_no[1],
    'v2_t': direction[1],
    "p1": direction[0],
    "p2": direction[1],
    "p1_dif" : dif_or_no[1],
    "Q1": direction[0],
    "Q2": direction[1],
    "Q1_diff": dif_or_no[1],
    "P1": direction[0],
    "P2": direction[1],
    "P1_diff": dif_or_no[1],

    }

def insert_image(image_path):
    def create_img(root, height = None, width = None, columnspan = None):

        canvas = tk.Canvas(root, height = height, width = width)  #height = 550, width = 1050
        canvas.create_image(0, 0, anchor = 'nw', image = img_compiled)
        return canvas

    img_compiled = tk.PhotoImage(file = image_path)
    return create_img

dir_images_for_cyl = str(Path(Path.cwd(), 'Cylinder', 'images'))

out_gor_1=insert_image(dir_images_for_cyl + '\zylhordausP.gif')
dif_gor_1 = insert_image(dir_images_for_cyl + '\dif_ zylhordausP.gif')
dif_ver_1 = insert_image(dir_images_for_cyl + '\dif_ ver_zylhordausP.gif')
in_gor_1 = insert_image(dir_images_for_cyl + '\zylhordeinM.gif')
gor_2 = insert_image(dir_images_for_cyl + '\zylhorgausP.gif')
ver_1_p1 = insert_image(dir_images_for_cyl + '\zyl_Verdaus_p1.gif')
ver_1_p2 = insert_image(dir_images_for_cyl + '\zyl_Verhdein_p2.gif')


def create_img_from_config():
    if metadata_cyl.get('config') != None:
        if metadata_cyl.get('config').get('direction') == 'p1':
            if metadata_cyl.get('config').get('arrangement') == "vertical movement":
               ver_1_p1(main_window).grid(row = 1, column=1)
            else:
                out_gor_1(main_window).grid(row = 1, column=1)

        elif metadata_cyl.get('config').get('direction') == 'p1_diff':
            if metadata_cyl.get('config').get('arrangement') == "vertical movement":
               dif_ver_1(main_window).grid(row = 1, column=1)
            else:
                dif_gor_1(main_window).grid(row = 1, column=1)

        elif metadata_cyl.get('config').get('direction') == 'p2':
            if metadata_cyl.get('config').get('arrangement') == "vertical movement":
               ver_1_p2(main_window).grid(row = 1, column=1)
            else:
                in_gor_1(main_window).grid(row = 1, column=1)



def option_input(*args, from_config = False, from_name_par = False):
    """
    создаем окно верхнего уровня (поверх основного)
    -для выбора опции и вывода соответсвующих изображений
    -для вывода пояснительного сообщения

    """
    window = tk.Toplevel()
    title_text = "ввод варианта"
    window.title(title_text)

    _type = tk.StringVar()

    def select_img_from_type_and_message():
        if metadata_cyl.get('config') == None:
            metadata_cyl['config'] = {}

        if _type.get() == direction[0] :
            out_gor_1(window).grid(row = 4, column=0)# , column = 0, columnspan= 1)
            dif_gor_1(window).grid(row = 4, column=1)
            metadata_cyl['config']['direction'] = 'p1'

        elif _type.get() == direction[1]:
            in_gor_1(window).grid(row = 4, column=0)
            gor_2(window).grid(row = 4, column=1)
            metadata_cyl['config']['direction'] = 'p2'

        if _type.get() == dif_or_no[0]:
            out_gor_1(window).grid(row = 4, column=0)

        elif _type.get() == dif_or_no[1]:
            dif_gor_1(window).grid(row = 4, column=0)
            metadata_cyl['config']['direction'] = 'p1_diff'


        if _type.get() == arrangement[0]:
            metadata_cyl['config']['arrangement']="horizontal movement"

            if metadata_cyl.get('config').get('direction') == 'p1' :
                out_gor_1(window).grid(row = 4, column=0)

            elif metadata_cyl.get('config').get('direction') == 'p1_diff' :
                dif_gor_1(window).grid(row = 4, column=0)

            elif metadata_cyl.get('config').get('direction') == 'p2' :
                in_gor_1(window).grid(row = 4, column=0)

        elif _type.get() == arrangement[1]:
            metadata_cyl['config']['arrangement'] = "vertical movement"

            if metadata_cyl.get('config').get('direction') == 'p1' :
                ver_1_p1(window).grid(row = 4, column=0)

            elif  metadata_cyl.get('config').get('direction') == 'p1_diff' :
                dif_ver_1(window).grid(row = 4, column=0)

            elif metadata_cyl.get('config').get('direction') == 'p2' :
                ver_1_p2(window).grid(row = 4, column=0)

        if from_config:
            lbl_text = None
            for key in args:
                if _type.get() == config.get(key):
                    lbl_text = 'Будет рассчитан параметр\n{:*^110}'.format(name_par.get(key))
                    break
                else:
                    lbl_text = '!!!параметр не определён'
            label = tk.Label(window, text = lbl_text, font=(font[0], 12),)
            label.grid(row=5,column = 0)

    def set_type_from_config(type):
            if metadata_cyl['config']['direction'] == 'p1':
                type.set(direction[0])
            elif metadata_cyl['config']['direction'] == 'p1_diff':
                type.set(dif_or_no[1])
            elif metadata_cyl['config']['direction'] == 'p2':
                type.set(direction[1])
    if from_config:
        for option_key  in sorted(args):
            radio = tk.Radiobutton(window, text = config.get(option_key),
                                   value = config.get(option_key),
                                   variable = _type,
                                   command = select_img_from_type_and_message ,
                                   font=(font[0], 12),)
            radio.grid()
        try:
            set_type_from_config(type= _type)
        except:
            _type.set(config.get(sorted(args)[0]))

    elif from_name_par:
        for option_key  in args:
            radio = tk.Radiobutton(window, text = name_par.get(option_key),
                                   value = option_key,
                                   variable = _type,
                                   font=(font[0], 12),)
            radio.grid()
        _type.set(args[0])

    else:
        for option  in args:
            radio = tk.Radiobutton(window, text = option,
                                   value = option,
                                   variable = _type,
                                   command = select_img_from_type_and_message ,
                                   font=(font[0], 12),)
            radio.grid()
        try:
            set_type_from_config(type= _type)
        except:
            _type.set(args[0])

    select_img_from_type_and_message()


    def clicked():
        w_to_file()
        create_img_from_config()
        window.destroy()

    button = tk.Button(window, text=' подтвердить выбор',
                    command=clicked,
                    font=(font[0], 12),
                    **btn_master)
    button.grid(row=7,column = 0)

    window.grab_set()
    window.wait_window()
    return _type.get()


def clicked_main_menu( lbl_result,from_config = False, from_name_par = False, **kwargs):
    """
    функция фабрики закрытия
    -для возможности выбора вариантов исполнения чего-либо
    -для вычисления и вывода полученного результата
    :param lbl_result: виджета для отображения результата
    :param kwargs: ключ - это имя параметра, значение - соответствующая функция
    """

    def clicked_():
        options_keys = (option_key for option_key in kwargs.keys())
        print('options_keys : ', options_keys)#--------------------------
        option = option_input(*options_keys, from_config= from_config, from_name_par= from_name_par)

        for key, funk in kwargs.items():
            if from_config:
                if option == config.get(key):
                    if type(funk) is FunctionType:
                        par = funk()
                        lbl_result.configure(text=par)
                    else:
                        lbl_result.configure(text='это не фунция')
                    break
            elif from_name_par:
                if option == key:
                    if type(funk) is FunctionType:
                        par = funk()
                        lbl_result.configure(text=par)
                    else:
                        lbl_result.configure(text='это не фунция')
                    break
        w_to_file()

    return clicked_
