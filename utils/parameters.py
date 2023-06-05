import tkinter as tk
import json
from repositories.my__init__ import SelectFiles
from sqlmodel import Session, select, col
from db.session import engine
from models import File

font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')

init_list_files = SelectFiles.all()
# запись
def update_file(path_file):
    def _w_file(_metadata):
        with open(path_file, 'w')as file:
            json.dump(_metadata, file, sort_keys=True, indent=4)
    return _w_file


# чтение
'''
def get_metadata_from_file(path_file):
    def _r_file():
        with open(path_file, 'r') as file:
            metadata  = json.load(file)#получаю словарь с внешнего файла
        return metadata
    return _r_file
'''

def get_metadata_from_file(file_id):
    def _get_metadata():
        with Session(engine) as session:
            _metadata = session.exec(select(File.meta_data).where(col(File.id) == file_id)).first()
            print('meta___data2222_________________', _metadata)
        #window_.destroy()
        return _metadata
    return _get_metadata
# ------------------for file_id_input------------------------------------------
 #---------------------------------------------------
file_id = None
def get_id_from_file(_file_id):
    global file_id
    def _get_id():
        global file_id
        file_id = _file_id
        print('def get_id_from_file(file_id):________________________', file_id)
        #window_.destroy()
        return file_id
    return _get_id
# ---------------------------------------------------

def file_id_input():
    global file_id

    window_ = tk.Tk()
    var=tk.IntVar()

    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window_.title(title_text)
    tk.Label(window_, text = lbl_text_message, font = (font[0],12)).grid(row = 0)
    lbl_error = tk.Label(window_, text=lbl_text_error, font=(font[0], 12), **btn_master)

    _row = 2
    for id, name in init_list_files:
        _row+=_row
        print('list_files___________________________________', init_list_files)
        tk.Button(window_,
                  text=name,
                  command=get_id_from_file(_file_id=id),
                  **btn_master).grid(column=0, row=_row)
    tk.Button(window_,
              text='ОТКРЫТЬ',
              command=lambda :window_.destroy(),
              **btn_master).grid(column=0, row=1000)
    print('_id_id_id_id_id_id1111-------------------------', file_id)
    window_.mainloop()
    print('_id_id_id_id_id_id2222-------------------------', file_id)
    return file_id

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
