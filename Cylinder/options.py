import tkinter as tk
from types import FunctionType
from pathlib import Path
from Cylinder.parameters import c,  btn_master, font, messages,w_file

main_window = tk.Tk()

direction = ('выдвижение штока (давление в поршневой полости)', 'втягивание штока (давление в штоковой полости)')
dif_or_no = ('обычная схема подключения(штоковая и поршневая полости разделены)', 'дифференциальная схема подлючения')
arrangement = ( 'горизонтальное расположение цилиндра', 'вертикальное расположение цилиндра\n либо расчет исходя из приведённой массы')

config = {
    "v1": direction[0],
    "v2": direction[1],
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

    }

def insert_image(image_path):
    def create_img(root, height = None, width = None, columnspan = None):
        '''
        label = tk.Label(root, image = img_compiled)
        label.grid(row = row, column = column, columnspan = columnspan)
        #label.grid_forget()
        '''
        canvas = tk.Canvas(root, height = height, width = width) #, height = 550, width = 1050
        canvas.create_image(0, 0, anchor = 'nw', image = img_compiled)
        return canvas
        #canvas.grid(row = row, column = column, columnspan = columnspan)


    img_compiled = tk.PhotoImage(file = image_path)
    return create_img


out_gor_1=insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'zylhordausP.gif')))
dif_gor_1 = insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'dif_ zylhordausP.gif')))
in_gor_1 = insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'zylhordeinM.gif')))
gor_2 = insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'zylhorgausP.gif')))
ver_1_p1 = insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'zyl_Verdaus_p1.gif')))
ver_1_p2 = insert_image(str(Path(Path.cwd(), 'Cylinder', 'images', 'zyl_Verhdein_p2.gif')))


def get_image_from_config():
    pass




def option_input(*args, message = False):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для выбора опции и вывода соответсвующих изображений
    для вывода пояснительного сообщения

    """
    window = tk.Toplevel()
    title_text = "ввод варианта"
    window.title(title_text)

    _type = tk.StringVar()

    def select_img_and_message():
        if c.get('config')==None:
            c['config'] = {}

        if _type.get() == direction[0] :
            out_gor_1(window).grid(row = 4, column=0)# , column = 0, columnspan= 1)
            dif_gor_1(window).grid(row = 4, column=1)
            c['config']['direction'] = 'p1 porshen'

        elif _type.get() == direction[1]:
            in_gor_1(window).grid(row = 4, column=0)
            gor_2(window).grid(row = 4, column=1)
            c['config']['direction'] = 'p2 shtock'

        if _type.get() == dif_or_no[0]:
            out_gor_1(window).grid(row = 4, column=0)
            c['config']['dif_or_no'] = 'no dif'
        elif _type.get() == dif_or_no[1]:
            dif_gor_1(window).grid(row = 4, column=0)
            c['config']['dif_or_no'] = 'differential'

        if _type.get() == arrangement[0]\
                and c.get('config').get('direction') == 'p1 porshen' :
            out_gor_1(window).grid(row = 4, column=0)
        elif _type.get() == arrangement[0]\
                and c.get('config').get('direction') == 'p2 shtock' :
            in_gor_1(window).grid(row = 4, column=0)
        elif _type.get() == arrangement[1]\
                and c.get('config').get('direction') == 'p1 porshen' :
            ver_1_p1(window).grid(row = 4, column=0)
        elif _type.get() == arrangement[1]\
                and c.get('config').get('direction') == 'p2 shtock' :
            ver_1_p2(window).grid(row = 4, column=0)

        if message:
            lbl_text = 'Петя'
            for key in args:

                if _type.get() == config.get(key):
                    lbl_text = 'Будет рассчитан параметр\n{:*^110}'.format(messages.get(key))
                    break
                else:
                    lbl_text = 'NNNNNNNNNNNNNNNNNo'
            label = tk.Label(window, text = lbl_text, font=(font[0], 12),)
            label.grid(row=5,column = 0)



    if message:
        for option_key  in sorted(args):
            radio = tk.Radiobutton(window, text = config.get(option_key),
                                   value = config.get(option_key),
                                   variable = _type,
                                   command = select_img_and_message ,
                                   font=(font[0], 12),)
            radio.grid()
        _type.set(config.get(sorted(args)[0]))

    else:
        for option  in args:
            radio = tk.Radiobutton(window, text = option,
                                   value = option,
                                   variable = _type,
                                   command = select_img_and_message ,
                                   font=(font[0], 12),)
            radio.grid()
        _type.set(args[0])
    select_img_and_message()

    def clicked():
        w_file()
        window.destroy()

    button = tk.Button(window, text=' подтвердить выбор',
                    command=clicked,
                    font=(font[0], 12),
                    **btn_master)
    button.grid(row=7,column = 0)

    window.grab_set()
    window.wait_window()

    return _type.get()


def clicked_main_menu( lbl_result,message = False, **kwargs):
    """
    функция фабрики закрытия
    -для возможности выбора вариантов исполнения чего-либо
    -для вычисления и вывода полученного результата
    :param lbl_result: виджета для отображения результата
    :param kwargs: ключ - это имя параметра, значение - соответствующая функция
    """

    def clicked_():
        print('kwargs          :::::',kwargs)
        options_keys = (option_key for option_key in kwargs.keys())
        option = option_input(*options_keys, message = message)
        for key, funk in kwargs.items():
            if option == config.get(key):
                if type(funk) is FunctionType:
                    par = funk()
                    lbl_result.configure(text=par)
                else:
                    lbl_result.configure(text='это не фунция')

    return clicked_
