import tkinter as tk
import json
from tkinter import filedialog


font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')


# запись
def w_metadata_to_file(path_file, metadata):
    def _w_file():
        with open(path_file, 'w')as file:
            json.dump(metadata, file, sort_keys=True, indent=4)
    return _w_file


# чтение
def r_from_file_to_metadata(path_file):
    def _r_file():
        with open(path_file, 'r') as file:
            metadata  = json.load(file)#получаю словарь с внешнего файла
        return metadata
    return _r_file



def file_name_input(initial_dir, metadata):
    window = tk.Tk()
    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window.title(title_text)
    tk.Label(window, text = lbl_text_message, font = (font[0],12)).grid(row = 0)
    lbl_error = tk.Label(window, text=lbl_text_error, font=(font[0], 12), **btn_master)

    options = dict(initialdir= initial_dir,
                   defaultextension=".json",
                   filetypes=[("JSON files", "*.json"),
                              ("TXT files", "*.txt"),
                              ("All files", "*.*")])

    def click_save():
        global _file_name
        _file_name = filedialog.asksaveasfilename(title='СОЗДАТЬ ФАЙЛ ДЛЯ ХРАНЕНИЯ ПАРАМЕТРОВ',
                                                 **options)
        if _file_name:
            w_metadata_to_file(path_file=_file_name, metadata=metadata)()
            window.destroy()
        else:
            lbl_error.grid(row=2, column=0)

    def click_open():
        global _file_name
        _file_name = filedialog.askopenfilename(title='ОТКРЫТЬ СУЩЕСТВУЮЩИЙ ФАЙЛ ДЛЯ ХРАНЕНИЯ ПАРАМЕТРОВ',
                                               **options)
        if _file_name:
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
    return _file_name


# ввод запрашиваемых значений и перезапись файла
def parameter_input(metadata, _name_par, _func_write):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """
    def _parameter_input(key,
                         message = None,
                         reference = None,
                         image_compiled = None):
            window_ = tk.Toplevel()
            title_text = "ввод параметра {}".format(_name_par.get(key))
            window_.title(title_text)



            default_text = '{} определён значением {}'.format(_name_par.get(key), metadata.get(key, 0)) + \
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
                    metadata[key] = par
                    _func_write()
                except:
                    par = metadata.get(key, 0)
                window_.destroy()
                return par

            lbl = tk.Label(window_, text=lbl_text,
                            font=(font[0], 12),
                            **btn_master)
            lbl.grid(column=0, row=0)

            ent = tk.Entry(window_, font=(font[0], 12))
            ent.grid(column=1, row=0)
            btn = tk.Button(window_, text=' подтвердить запись',
                            command=clicked,
                            font=(font[0], 12),
                            **btn_master)
            btn.grid(column=0, row=1)

            window_.grab_set()
            window_.wait_window()  #запускает локальный цикл событий, который
                                   # завершается после уничтожения окна
            return par
    return _parameter_input
