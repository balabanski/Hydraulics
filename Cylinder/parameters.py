import json
import tkinter as tk
from types import FunctionType
from pathlib import Path
from tkinter import filedialog


font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')

c = {}

messages = {
    "F1": 'F1 (см2) -площадь поршня ',
    "F2": 'F2 (см2) -пплощадь кольцевого сечения',
    "d1": 'd1 (мм)-диаметр поршня ',
    "d2": 'd2 (мм)-диаметр штока ',
    "t1": 't1 (сек)-время выдвижения штока',
    "t2": 't2 (сек)-время втягивания штока',
    "v1": "v1 (м/сек)скорость при выдвижении штока ",
    "v2": "v2 (м/сек)скорость при втягивании штока ",
    "Q1": "Q1 (л/мин)- требуемая подача в поршневую полость",
    "Q2": "Q2 (л/мин)- требуемая подача в штоковую полость",
    "Q1_diff": "Q1_diff (л/мин)- (при дифференциальной схеме)требуемая подача при выдвижении штока",
    "P1": 'P1 (кН) - усилие при выдвижении штока',
    "P2": 'P2 (кН) - усилие при втягивании штока',
    "m": 'm (тн) - масса груза',
    "p1": 'p1 (Bar) - давление в поршневой полости',
    "p2": 'p2 (Bar) - давление в штоковой полости',
    "L1": 'L 1(мм)- ход поршня при выдвижении штока ',
    "L2": 'L 2(мм)- ход поршня при втягивании штока ',
    "a": 'a(м/с2) - ускорение',
    "message_d2": 'что бы ВВЕСТИ значение  усилия (кН)- жми 1\n\
               что бы ВЫЧИСЛИТЬ значение  усилия - жми 2\n '
}


def file_name_input():
    window = tk.Tk()
    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window.title(title_text)
    tk.Label(window, text = lbl_text_message, font = (font[0],12)).grid(row = 0)
    lbl_error = tk.Label(window, text=lbl_text_error, font=(font[0], 12), **btn_master)

    options = dict(initialdir=str(Path(Path.cwd(), 'Cylinder', 'JsonFiles')),
                   defaultextension=".json",
                   filetypes=[("JSON files", "*.json"),
                              ("TXT files", "*.txt"),
                              ("All files", "*.*")])

    def click_save():
        global file_name
        file_name = filedialog.asksaveasfilename(title='СОЗДАТЬ ФАЙЛ ДЛЯ ХРАНЕНИЯ ПАРАМЕТРОВ',
                                                 **options)
        if file_name:
            w_file()
            window.destroy()
        else:
            lbl_error.grid(row=2, column=0)

    def click_open():
        global file_name
        file_name = filedialog.askopenfilename(title='ОТКРЫТЬ СУЩЕСТВУЮЩИЙ ФАЙЛ ДЛЯ ХРАНЕНИЯ ПАРАМЕТРОВ',
                                               **options)
        if file_name:
            window.destroy()
        else:
            lbl_error.grid(row=2, column=0)


    btn_open = tk.Button(window, text='открыть файл', font=(font[0], 12),
                         command=click_open, **btn_master)
    btn_open.grid(row=1, column=0)
    btn_create = tk.Button(window, text='создать файл', font=(font[0], 12),
                           command=click_save, **btn_master)
    btn_create.grid(row=1, column=1)

    window.mainloop()
    return file_name


# запись
def w_file():
    with open(file_name, 'w')as file:
        json.dump(c, file, sort_keys=True, indent=4)


# чтение   
def r_file():
    with open(file_name, 'r') as file:
        c_read = json.load(file)
    for key, val in c_read.items():
        c[key] = val
        if c[key] != 0:
            print('    {}:{:>2}'.format(key, val))


# получаю словарь из внешнего фаила или записываю
def get_par():
    try:
        r_file()
    except:
        print("запись имеющихся  значений в файл {}".format(file_name))
        w_file()







def option_input(*options):

    """
    сосдаем окно верхнего уровня (поверх основного)
    для выбора опции
    """
    window = tk.Toplevel()
    title_text = "ввод варианта"
    window.title(title_text)

    _type = tk.StringVar()
    for name_option  in options:
        radio = tk.Radiobutton(window, text = name_option,
                               value = name_option,
                               variable = _type,
                               font=(font[0], 12),)
        radio.grid()

    _type.set(options[0])

    def clicked():
        window.destroy()

    button = tk.Button(window, text=' подтвердить выбор',
                    command=clicked,
                    font=(font[0], 12),
                    **btn_master)
    button.grid()
    window.grab_set()
    window.wait_window()  #запускает локальный цикл событий, который
                          # завершается после уничтожения окна

    return _type.get()



def insert_image(root, image_path):
    canvas = tk.Canvas(root, height = 550, width = 1050)
    img = tk.PhotoImage(file = image_path)
    image = canvas.create_image(0, 0, anchor = 'nw', image = img)
    canvas.grid()
    root.grab_set()
    root.wait_window()



# ввод запрашиваемых значений и перезапись файла
def parameter_input(key, message = None, reference = None, image_path = None):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """

    title_text = "ввод параметра {}".format(messages.get(key))

    default_text = '{} определён значением {}'.format(messages.get(key), c.get(key, 0)) + \
                    '\n (можешь ввести новое значение в поле справа' + \
                    '\n либо ничего не вводить и оставить прежним)'
    lbl_text = default_text
    if message  :
        lbl_text = '{}\n{}'.format(message, lbl_text)
    if reference :
        lbl_text = '{}\n\n{}'.format(lbl_text, reference )

    def clicked():
        global par
        try:
            par = float(ent.get())
            c[key] = par
            w_file()  # перезаписываю файл
        except:
            par = c.get(key, 0)
        window_.destroy()


    window_ = tk.Toplevel()
    window_.title(title_text)
    lbl = tk.Label(window_, text=lbl_text,
                    font=(font[0], 12),
                    **btn_master)
    lbl.grid(column=0, row=0)

    ent = tk.Entry(window_, font=(font[0], 12))
    ent.grid(column=1, row=0)
    btn = tk.Button(window_, text=' подтвердить запись',
                    command=clicked,
                    font=(font[0], 12))
    btn.grid(column=0, row=1)

    if image_path :
        insert_image(window_, image_path)
    else:
        window_.grab_set()
        window_.wait_window()  #запускает локальный цикл событий, который
                            # завершается после уничтожения окна
    return par


def clicked_main_menu(row_, lbl_result, **kwargs):
    """
    функция фабрики закрытия - расширяем текущее окно дополнительными виджетами
    -для возможности выбора вариантов исполнения чего-либо
    -для вычисления и вывода полученного результата
    :param row_: просто номер строки (для отображения виджет)
    :param lbl_result: виджета для отображения результата
    :param kwargs: ключ - это имя параметра, значение - соответствующая функция
    """

    def clicked_():
        row = row_
        _types = [messages[key] for key, funk in sorted(kwargs.items())]
        _type = tk.StringVar()
        _type.set(_types[0])
        radios = [tk.Radiobutton(text=t, value=t, variable=_type, font=(font[0], 12)) for t in _types]
        for radio in radios:
            row = row + 1
            radio.grid(column=0, row=row)

        def click():
            for key, funk in kwargs.items():
                if _type.get() == messages[key]:
                    if type(funk) is FunctionType:
                        par = funk()
                        lbl_result.configure(text=par)
                    else:
                        lbl_result.configure(text='это не фунция')

        btn = tk.Button(text='подтвердить выбор', font=(font[0], 12),
                        command=click, **btn_master)
        btn.grid(column=0, row=row + 1)
        print(row)
    return clicked_
