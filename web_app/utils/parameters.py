import asyncio
import tkinter as tk

from web_app.requests.req_file import create_file, delete_file, get_list_files, update_file
from web_app.user import GUI_login, get_token
from web_app.utils.settings_gui import btn_master, btn_master_2, font


file_id = None
file_name = None


# ---------------------------------------------------
def gui_filedialog():
    token = get_token()

    print("****************in filedialog**init_list_files************************")
    init_list_files = asyncio.run(get_list_files(token_=token))
    print("init_list_files =__________________________________________", init_list_files)

    # ------------------for file_id_input------------------------------------------
    global file_id
    global file_name

    window_ = tk.Tk()
    title_text = "открыть или создать файл для хранения параметров"
    window_.title(title_text)

    if init_list_files is not None:
        lbl_text = " Для работы необходимо " + title_text
        tk.Label(window_, text=lbl_text, font=(font[0], 12)).grid(row=0)
    else:
        lbl_text = "Похоже ваш токен устарел.\n Закройте это окно, пройдите авторизацию, и повторите попытку."
        tk.Label(window_, text=lbl_text, font=(font[0], 12)).grid(row=0)

        login_ = GUI_login(root=tk.Tk())
        login_.setup_login()
        login_.start()
        raise Exception("повторить действия")

    # but = None
    def click_name_(_file_id, _file_name, row_) -> int:
        def _get_id():
            global file_id
            global file_name

            file_id = _file_id
            file_name = _file_name
            print("file_id, file_name__________________", file_id, file_name)
            but_open.configure(text=f"ОТКРЫТЬ {file_name}")
            but_open.grid(column=0, row=1000)
            but_del.configure(text=f"УДАЛИТЬ {file_name}")
            but_del.grid(column=0, row=1005)

        return _get_id

    _row = 2
    for i in init_list_files:
        _row += 1
        tk.Button(
            window_,
            # text=i['name'] + f"  (id={i['id']})",
            text=f"{i[1]} (id={i[0]})".center(28, " "),
            command=click_name_(_file_id=i[0], _file_name=i[1], row_=_row),
            **btn_master_2,
        ).grid(column=0, row=_row)

    but_open = tk.Button(
        window_,
        command=lambda: window_.destroy(),
        **btn_master,
    )

    ent = tk.Entry(window_, font=(font[0], 12))
    ent.grid(column=0, row=1001)

    def create_file_click():
        name_ = ent.get()
        print("****************CREATE**************************")
        for tuple_ in init_list_files:
            if name_ in tuple_:
                raise Exception(f"фаил с именем {name_} уже существует")
        if name_:
            new_file = create_file(name_=name_)
            global file_id
            global file_name
            file_id = new_file.get("id")
            file_name = name_
        window_.destroy()

    tk.Button(window_, text="СОЗДАТЬ", command=create_file_click, **btn_master).grid(
        column=1, row=1001
    )

    def delete_file_click():
        window_.destroy()
        delete_file(id_=file_id)
        gui_filedialog()

    but_del = tk.Button(window_, command=delete_file_click, **btn_master)

    window_.mainloop()

    return [file_id, file_name]


# ввод запрашиваемых значений и перезапись файла
def gui_parameter_input(metadata, _name_par, _file_id, _file_name) -> float:
    """
    сосдаем окно верхнего уровня (поверх основного)
    для ввода необходимых параметров и записи их во внешний файл
    """

    def _parameter_input(key, message=None, reference=None, func_widget_image=None):
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

        if func_widget_image:
            func_widget_image(window_, height=550, width=1050).grid(row=6, column=0)

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
        ent.focus()
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
