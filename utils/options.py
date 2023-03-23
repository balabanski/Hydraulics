import tkinter as tk
from utils.parameters import  btn_master, font
from types import FunctionType

def insert_image(image_path):
    def create_img(root, height = None, width = None, columnspan = None):

        canvas = tk.Canvas(root, height = height, width = width)  #height = 550, width = 1050
        canvas.create_image(0, 0, anchor = 'nw', image = img_compiled)
        return canvas

    img_compiled = tk.PhotoImage(file = image_path)
    return create_img



"""
создаем окно верхнего уровня (поверх основного)
-для выбора опции и вывода соответсвующих изображений
-для вывода пояснительного сообщения
from debug import debug
@debug
"""
def option_input(func_img_from_type=None,
                 func_create_img_from_config= None,
                 func_set_type_from_config= None,
                 config_json= None,
                 name_par_json= None,
                 ):
    def _option_input(*args,
                      from_config = False, message = False, from_name_par = False):
        window = tk.Toplevel()
        title_text = "ввод варианта"
        window.title(title_text)

        _type = tk.StringVar()

        def select_img_and_message_from_type():
            if func_img_from_type:
                func_img_from_type(window, _type)
            if message:
                lbl_text= None
                for key in args:
                    if _type.get() == config_json.get(key):
                        lbl_text = 'Будет рассчитан параметр\n{:*^110}'.format(name_par_json.get(key))
                        break
                    else:
                        lbl_text = '!!!параметр не определён'
                label = tk.Label(window, text = lbl_text, font=(font[0], 12),)
                label.grid(row=10, column = 0)

        if from_config:
            for option_key  in sorted(args):

                radio = tk.Radiobutton(window, text = config_json.get(option_key),
                                       value = config_json.get(option_key),
                                       variable = _type,
                                       command = select_img_and_message_from_type ,
                                       font=(font[0], 12),)
                radio.grid()
            try:
                func_set_type_from_config(type= _type)
                select_img_and_message_from_type()
            except:
                _type.set(config_json.get(sorted(args)[0]))

        elif from_name_par:
            for key_par  in args:
                radio = tk.Radiobutton(window, text = name_par_json.get(key_par),
                                       value = key_par,
                                       variable = _type,
                                       font=(font[0], 12),)
                radio.grid()
            _type.set(args[0])

        else:
            for option in sorted(args):
                radio = tk.Radiobutton(window, text = option,
                                       value = option,
                                       variable = _type,
                                       # экземпляр функции select_img_from_type_and_message(for cylinder)
                                       command = select_img_and_message_from_type ,
                                       font=(font[0], 12),)
                radio.grid()
            try:
                func_set_type_from_config(type= _type)
                select_img_and_message_from_type()
            except:
                _type.set(args[0])

        def clicked():
            func_create_img_from_config()
            window.destroy()

        button = tk.Button(window, text=' подтвердить выбор',
                        command=clicked,
                        font=(font[0], 12),
                        **btn_master)
        button.grid(row=7,column = 0)

        window.grab_set()
        window.wait_window()
        return _type.get()

    return _option_input



def clicked_main_menu(funk_option_input, func_write_to_file, config_json ):
    """
    функция фабрики закрытия
    -для возможности выбора вариантов исполнения чего-либо
    -для вычисления и вывода полученного результата
    :param lbl_result: виджета для отображения результата
    :param kwargs: ключ - это имя параметра, значение - соответствующая функция
    """
    def _clicked_main_menu(lbl_result,
                           from_config = False, message = False,  from_name_par = False,
                           **kwargs):
        def clicked_():
            options_keys = (option_key for option_key in kwargs.keys())
            #print('options_keys : ', *options_keys)-*-после
            # распаковки генератора все исчезает(?!)
            option = funk_option_input(*options_keys, from_config= from_config, message = message, from_name_par= from_name_par)
            for key, funk in kwargs.items():
                if from_config:
                    if option == config_json.get(key):
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
            func_write_to_file()
        return clicked_
    return _clicked_main_menu

