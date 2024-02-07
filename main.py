import tkinter as tk
from web_app.user import user_file, gui_auto_login, GUI_login, get_token, read_user_data
from web_app.utils.settings_gui import font, btn_master
import os

def gui_cyl_motor_pump():
    main_window = tk.Tk()
    main_window.title("Расчет гидравлических параметров")

    def click_cyl():
        main_window.destroy()
        import web_app.Cylinder.app

    def click_mot():
        main_window.destroy()
        import web_app.Motor.app

    def click_pump():
        main_window.destroy()
        import web_app.Pump.app

    btn_cyl = tk.Button(main_window, text='ГИДРОЦИЛЛИНДР',
                        font=(font[0], 12),
                        command=click_cyl,
                        **btn_master)
    btn_mot = tk.Button(main_window, text='ГИДРОМОТОР',
                        font=(font[0], 12),
                        command=click_mot,
                        **btn_master)
    btn_pump = tk.Button(main_window, text='ГИДРОНАСОС',
                         font=(font[0], 12),
                         command=click_pump,
                         **btn_master)
    btn_cyl.grid(column=0, row=1)
    btn_mot.grid(column=1, row=1)
    btn_pump.grid(column=2, row=1)

    main_window.mainloop()


if __name__ == "__main__":
    try:
        data_user = read_user_data()
        print("data_user ===========", data_user)
        token = data_user["token"]

        if token is None:
            raise Exception
        email = data_user["email"]
        gui_auto_login(token_=token, email_=email)

        token = get_token()

    except:
        login_ = GUI_login(root=tk.Tk())
        data__ = login_.setup_login()
        login_.start()

        token = get_token()

    if token:
        gui_cyl_motor_pump()



