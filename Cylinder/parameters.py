import json
from tkinter import filedialog
import tkinter as tk
from pathlib import Path

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
    "Q1": "Q1 (л/мин)- требуемая подача в поршневую полость (при выдвижении штока)",
    "Q2": "Q2 (л/мин)- требуемая подача в штоковую полость(при втягивании штока)",
    "Q1_diff": "Q1_diff (л/мин)- (при дифференциальной схеме)требуемая подача при выдвижении штока",
    "P1": 'P1 (кН) - усилие при выдвижении штока',
    "P2": 'P2 (кН) - усилие при втягивании штока',
    "m": 'm (тн) - масса груза',
    "p1": 'p1 (Bar) - давление в поршневой полости (при выдвижении штока)',
    "p1_dif": 'p1_dif (Bar) - (при дифференциальной схеме)давление в поршневой полости (при выдвижении штока)',
    "p2": 'p2 (Bar) - давление в штоковой полости (при втягивании штока)',
    "L1": 'L 1(мм)- ход поршня при выдвижении штока ',
    "L2": 'L 2(мм)- ход поршня при втягивании штока ',
    "a": 'a(м/с2) - ускорение',

}


# запись
def w_file():
    with open(file_name, 'w')as file:
        json.dump(c, file, sort_keys=True, indent=4)


# чтение
def r_file():
    with open(file_name, 'r') as file:
        c_read = json.load(file)#получаю словарь с внешнего файла
    for key, val in c_read.items():
        c[key] = val


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

file_name = file_name_input()


# ввод запрашиваемых значений и перезапись файла
def parameter_input(key, message = None, reference = None, image_compiled = None):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """
    window_ = tk.Toplevel()
    title_text = "ввод параметра {}".format(messages.get(key))
    window_.title(title_text)



    default_text = '{} определён значением {}'.format(messages.get(key), c.get(key, 0)) + \
                    '\n (можешь ввести новое значение в поле справа' + \
                    '\n либо ничего не вводить и оставить прежним)'
    lbl_text = default_text
    if message  :
        lbl_text = '{}\n{}'.format(message, lbl_text)
    if reference :
        lbl_text = '{}\n\n{}'.format(lbl_text, reference )

    if image_compiled:
        image_compiled(window_,height = 550, width = 1050).grid(row = 6, column = 0)

    def clicked():
        global par
        try:
            par = float(ent.get())
            c[key] = par
            w_file()  # перезаписываю файл
        except:
            par = c.get(key, 0)
        window_.destroy()

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

    window_.grab_set()
    window_.wait_window()  #запускает локальный цикл событий, который
                            # завершается после уничтожения окна
    return par