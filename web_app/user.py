import json
import os
import tkinter as tk

from web_app.requests.req_user import req_access_token, sign_up, update_user_me
from web_app.utils.settings_gui import btn_master, font


token = None

# from __future__ import annotations


email = None


def create_user_folder():
    home_folder = os.path.expanduser("~")
    hydr_folder = os.path.join(home_folder, "hydraulics_user_data")

    if os.path.exists(hydr_folder) == 0:
        os.mkdir(hydr_folder)
    return hydr_folder


user_file = os.path.join(create_user_folder(), "hydr_user_data.json")


def write_user_data(data_user: dict, path: str):
    with open(path, "w") as file:
        json.dump(data_user, file, indent=4)


def read_user_data():
    with open(user_file, "r") as file:
        data_user = json.load(file)
    return data_user


def remove_user_dada():
    try:
        os.remove(user_file)
    except:
        pass


class GUI_login:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Авторизация")

    def setup_login(self):
        lbl_email = tk.Label(self.root, text="Ваш email", font=(font[0], 12), **btn_master)
        lbl_email.grid(column=0, row=1)

        lbl_password = tk.Label(self.root, text="пароль", font=(font[0], 12), **btn_master)
        lbl_password.grid(column=0, row=3)

        entr_email = tk.Entry(self.root, font=(font[0], 12))
        entr_email.grid(column=1, row=1)

        entr_password = tk.Entry(self.root, font=(font[0], 12))
        entr_password.grid(column=1, row=3)

        lbl_message_ok = tk.Label(self.root, text=" " * 100, font=(font[0], 12), **btn_master)
        lbl_message_ok.grid(column=1, row=5)

        def click_sign_in():
            global token
            global email

            email = entr_email.get()
            password = entr_password.get()

            if email and password:
                try:
                    token = req_access_token(email_=email, password_=password)

                    write_user_data(data_user={"email": email, "token": token}, path=user_file)
                    self.root.destroy()
                except:
                    lbl_message_ok.configure(text="***неправильный пароль или email***")
                    pass

        def click_sign_up():
            self.root.destroy()
            new_user = GUI_create(token_=None, email_=None)
            new_user.setup()
            new_user.start()

        btn_sign_in = tk.Button(
            self.root,
            text="войти",
            font=(font[0], 12),
            command=click_sign_in,
            **btn_master,
        )
        btn_sign_in.grid(column=0, row=8)

        btn_sign_up = tk.Button(
            self.root,
            text="Регистрация",
            font=(font[0], 12),
            command=click_sign_up,
            **btn_master,
        )
        btn_sign_up.grid(column=0, row=10)

    def start(self) -> None:
        self.root.mainloop()


class GUI_update_or_create:
    def __init__(self, token_, email_):
        self.token = token_
        self.email = email_

    titl_text: str
    btn_text: str
    update_user: bool = False
    create_user: bool = False

    def setup(self):
        self.root = tk.Tk()
        self.root.title(self.titl_text)
        lbl_email = tk.Label(self.root, text="Ваш email", font=(font[0], 12), **btn_master)
        lbl_email.grid(column=0, row=1)

        lbl_password = tk.Label(self.root, text="пароль", font=(font[0], 12), **btn_master)
        lbl_password.grid(column=0, row=3)

        entr_email = tk.Entry(self.root, font=(font[0], 12))
        entr_email.grid(column=1, row=1)

        entr_password = tk.Entry(self.root, font=(font[0], 12))
        entr_password.grid(column=1, row=3)

        lbl_message_ok = tk.Label(self.root, text=" " * 100, font=(font[0], 12), **btn_master)
        lbl_message_ok.grid(column=1, row=5)

        lbl_check_repeat_password = tk.Label(
            self.root, text="повторить пароль", font=(font[0], 12), **btn_master
        )
        lbl_check_repeat_password.grid(column=0, row=4)

        entr_check_repeat_password = tk.Entry(self.root, font=(font[0], 12))
        entr_check_repeat_password.grid(column=1, row=4)

        def get_data():
            data = {}
            email = entr_email.get()
            password = entr_password.get()
            check_repeat_password = entr_check_repeat_password.get()
            if email:
                data["email"] = email
            else:
                data["email"] = self.email
            if password != check_repeat_password:
                text = "неверный ввод пароля"
                lbl_message_ok.configure(text=text.center(100, "*"))
                raise RuntimeError(text)
            if password and check_repeat_password:
                data["password"] = password
                data["repeat_password"] = check_repeat_password

            print("\n", "token___________", self.token, "\n", "data___________", data)
            return data

        def click_update_user():
            data = get_data()
            res = update_user_me(token_=self.token, data_=data)  # user.id

            if res:
                text = "успешно. Закройте окно"
                lbl_message_ok.configure(text=text.center(100, "*"))

                data_user = {"token": self.token, "email": data["email"]}
                write_user_data(data_user=data_user, path=user_file)

            else:
                text = "Ошибка. Проверьте введённые данные."
                lbl_message_ok.configure(text=text.center(100, "*"))
                raise RuntimeError(text)

        def click_create_user():
            data = get_data()
            data_user = {"user": data}
            print("data_user______________________", data_user)

            res: dict = sign_up(data_=data_user)
            print("res = sign_up____________________", res)

            if res:
                if res.get("email"):
                    text = "успешно. Закройте окно и войдите в систему"
                    lbl_message_ok.configure(text=text.center(100, "*"))
                    login = GUI_login(root=tk.Tk())
                    login.setup_login()
                    login.start()

                elif res.get("detail"):
                    text = str(res["detail"])

                    lbl_message_ok.configure(text=text.center(100, "*"))
                    raise Exception(text)

            else:
                text = "Ошибка. Проверьте введённые данные."
                lbl_message_ok.configure(text=text.center(100, "*"))
                raise RuntimeError(text)

        if self.update_user:
            func_click = click_update_user

        if self.create_user:
            func_click = click_create_user

        btn_sign_in = tk.Button(
            self.root,
            text=self.btn_text,
            font=(font[0], 12),
            command=func_click,
            **btn_master,
        )
        btn_sign_in.grid(column=0, row=8)

    def start(self):
        self.root.mainloop()


class GUI_update(GUI_update_or_create):
    titl_text = "Обновление"
    btn_text = "подтвердить изменения"
    update_user = True


class GUI_create(GUI_update_or_create):
    titl_text = "Регистрация нового пользователя"
    btn_text = "Зарегистрироваться"
    create_user = True


def gui_auto_login(token_, email_):
    global token
    global email
    token = token_
    email = email_

    user_window = tk.Tk()
    user_window.title("Авторизация")

    def click_auto_sign_in():
        user_window.destroy()

    btn_auto_sign_in = tk.Button(
        user_window,
        text=f"ВОЙТИ как пользователь {email_}",
        font=(font[0], 12),
        command=click_auto_sign_in,
        **btn_master,
    )
    btn_auto_sign_in.grid(column=0, row=2)

    def click_update_user():
        user_window.destroy()
        update = GUI_update(token_=token_, email_=email_)
        update.setup()
        update.start()

    def click_log_out():
        global token
        token = None
        user_window.destroy()
        remove_user_dada()

    btn_update_user = tk.Button(
        user_window,
        text="МЗМЕНИТЬ ПАРОЛЬ, EMAIL",
        font=(font[0], 12),
        command=click_update_user,
        **btn_master,
    )
    btn_update_user.grid(column=0, row=3)

    btn_log_out = tk.Button(
        user_window,
        text="ВЫЙТИ",
        font=(font[0], 12),
        command=click_log_out,
        **btn_master,
    )
    btn_log_out.grid(column=0, row=4)

    user_window.mainloop()


def get_email():
    return email


def get_token():
    return token
