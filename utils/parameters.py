import tkinter as tk

from sqlmodel import select, col
from src.db.session import engine
from models import File
import asyncio

from src.repositories.file import update_file, create_file, delete_file, select_file
from src.schemas import IFileUpdateSchema, IFileCreateSchema

font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#4444ff',
                  fg='#ffffff', activeforeground='#ffffff')

init_list_files = asyncio.run(select_file())


# ------------------for file_id_input------------------------------------------

file_id = None


def click_name_(_file_id):
    global file_id

    def _get_id():
        global file_id
        file_id = _file_id
        print('def get_id_from_file(file_id):________________________', file_id)
        return file_id
    return _get_id


# ---------------------------------------------------

def file_id_input():
    global file_id

    window_ = tk.Tk()
    var = tk.IntVar()

    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window_.title(title_text)
    tk.Label(window_, text=lbl_text_message, font=(font[0], 12)).grid(row=0)
    lbl_error = tk.Label(window_, text=lbl_text_error, font=(font[0], 12), **btn_master)

    _row = 2
    for id_, name in init_list_files:
        _row += _row
        tk.Button(window_,
                  text=name+f" ----id={id_}",
                  command=click_name_(_file_id=id_),
                  **btn_master).grid(column=0, row=_row)

    def open_file_click():
        window_.destroy()

    tk.Button(window_,
              text='ОТКРЫТЬ',
              # command=lambda: open_file_click(),
              command=lambda: window_.destroy(),
              **btn_master).grid(column=0, row=1000)

    ent = tk.Entry(window_, font=(font[0], 12))
    ent.grid(column=0, row=1001)

    def create_file_click():
        global init_list_files
        name_ = ent.get()
        asyncio.run(create_file(file=IFileCreateSchema(name=name_)))
        window_.destroy()
        init_list_files = asyncio.run(select_file())

        file_id_input()
        # func_init_list_files(list_files=init_list_files)

    tk.Button(window_,
              text='СОЗДАТЬ',
              command=create_file_click,
              **btn_master).grid(column=1, row=1001)

    def delete_file_click():
        global init_list_files
        window_.destroy()
        asyncio.run(delete_file(file_id=file_id))
        init_list_files = asyncio.run(select_file())
        file_id_input()

    tk.Button(window_,
              text='УДАЛИТЬ',
              command=delete_file_click,
              **btn_master).grid(column=0, row=1005)

    window_.mainloop()

    return file_id


# ввод запрашиваемых значений и перезапись файла
def parameter_input(metadata, _name_par, file_name):
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """

    def _parameter_input(key,
                         message=None,
                         reference=None,
                         image_compiled=None):
        window_ = tk.Toplevel()
        title_text = "ввод параметра {}".format(_name_par.get(key))
        window_.title(title_text)

        default_text = '{} определён значением {}'.format(_name_par.get(key), metadata.get(key, 0)) + \
                       '\n (можешь ввести новое значение в поле справа' + \
                       '\n либо ничего не вводить и оставить прежним)'
        lbl_text = default_text
        if message:
            lbl_text = '{}\n{}'.format(message, lbl_text)
        if reference:
            lbl_text = '{}\n\n{}'.format(lbl_text, reference)

        if image_compiled:
            image_compiled(window_, height=550, width=1050).grid(row=6, column=0)

        def clicked():
            global par
            if ent.get():
                par = float(ent.get())
                metadata[key] = par
            par = metadata.get(key, 0)
            asyncio.run(update_file(file_id=file_name, file=IFileUpdateSchema(meta_data=metadata)))

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
        window_.wait_window()  # запускает локальный цикл событий, который
        # завершается после уничтожения окна
        return par

    return _parameter_input
