import asyncio
import tkinter as tk

from web_app.requests.req_file import create_file, delete_file, get_list_files, update_file
from web_app.user import get_token
from web_app.utils.settings_gui import btn_master, font


file_id = None
file_name = None


def click_name_(_file_id, _file_name) -> int:
    def _get_id():
        global file_id
        global file_name
        file_id = _file_id
        file_name = _file_name
        print("file_id, file_name__________________", file_id, file_name)

    return _get_id


# ---------------------------------------------------
def gui_filedialog():
    global init_list_files
    token = get_token()

    init_list_files = asyncio.run(get_list_files(token_=token))
    print("init_list_files =__________________________________________", init_list_files)

    # ------------------for file_id_input------------------------------------------
    global file_id
    global file_name

    window_ = tk.Tk()

    title_text = "открыть или создать файл для хранения параметров"
    lbl_text_error = "Для работы необходимо " + title_text
    lbl_text_message = lbl_text_error + "\nвыбери вариант"

    window_.title(title_text)
    tk.Label(window_, text=lbl_text_message, font=(font[0], 12)).grid(row=0)
    lbl_error = tk.Label(window_, text=lbl_text_error, font=(font[0], 12), **btn_master)

    _row = 2
    for i in init_list_files:
        _row += _row
        tk.Button(
            window_,
            # text=i['name'] + f"  (id={i['id']})",
            text=i[1] + f"  (id={i[0]})",
            command=click_name_(_file_id=i[0], _file_name=i[1]),
            **btn_master,
        ).grid(column=0, row=_row)

    tk.Button(
        window_,
        text="ОТКРЫТЬ",
        # command=lambda: open_file_click(),
        command=lambda: window_.destroy(),
        **btn_master,
    ).grid(column=0, row=1000)

    ent = tk.Entry(window_, font=(font[0], 12))
    ent.grid(column=0, row=1001)

    def create_file_click():
        name_ = ent.get()
        print("****************CREATE**************************")
        create_file(name_=name_)
        window_.destroy()
        print("****************in CREATE**init_list_files************************")
        # init_list_files = asyncio.run(get_list_files())

        gui_filedialog()
        # func_init_list_files(list_files=init_list_files)

    tk.Button(window_, text="СОЗДАТЬ", command=create_file_click, **btn_master).grid(
        column=1, row=1001
    )

    def delete_file_click():
        window_.destroy()
        delete_file(id_=file_id)
        gui_filedialog()

    tk.Button(window_, text="УДАЛИТЬ", command=delete_file_click, **btn_master).grid(
        column=0, row=1005
    )

    window_.mainloop()

    return [file_id, file_name]


# ввод запрашиваемых значений и перезапись файла
def parameter_input(metadata, _name_par, _file_id, _file_name) -> float:
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """

    def _parameter_input(key, message=None, reference=None, image_compiled=None):
        window_ = tk.Toplevel()
        title_text = "ввод параметра {}".format(_name_par.get(key))
        window_.title(title_text)

        default_text = (
            "{} определён значением {}".format(_name_par.get(key), metadata.get(key, 0))
            + "\n (можешь ввести новое значение в поле справа"
            + "\n либо ничего не вводить и оставить прежним)"
        )
        lbl_text = default_text
        if message:
            lbl_text = "{}\n{}".format(message, lbl_text)
        if reference:
            lbl_text = "{}\n\n{}".format(lbl_text, reference)

        if image_compiled:
            image_compiled(window_, height=550, width=1050).grid(row=6, column=0)

        def clicked():
            global par
            if ent.get():
                par = float(ent.get())
                metadata[key] = par
            par = metadata.get(key, 0)
            update_file(id_=_file_id, name=_file_name, meta_data=metadata)

            window_.destroy()
            return par

        lbl = tk.Label(window_, text=lbl_text, font=(font[0], 12), **btn_master)
        lbl.grid(column=0, row=0)

        ent = tk.Entry(window_, font=(font[0], 12))
        ent.grid(column=1, row=0)
        btn = tk.Button(
            window_,
            text=" подтвердить запись",
            command=clicked,
            font=(font[0], 12),
            **btn_master,
        )
        btn.grid(column=0, row=1)

        window_.grab_set()
        window_.wait_window()  # запускает локальный цикл событий, который
        # завершается после уничтожения окна
        return par

    return _parameter_input
