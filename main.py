import tkinter as tk
from utils.parameters import font,btn_master

main_window = tk.Tk()

main_window.title("Расчет гидравлических параметров")

def click_cyl():
    main_window.destroy()
    import Cylinder.app


btn_cyl = tk.Button(main_window, text='ГИДРОЦИЛЛИНДР',
                font=(font[0], 12),
                command = click_cyl,
                **btn_master)
btn_cyl.grid(column=0, row=1)



def click_mot():
    main_window.destroy()
    import Motor.app

btn_cyl = tk.Button(main_window, text='ГИДРОМОТОР',
                font=(font[0], 12),
                command = click_mot,
                **btn_master)
btn_cyl.grid(column=1, row=1)



def click_pump():
    main_window.destroy()
    import Pump.app

btn_cyl = tk.Button(main_window, text='ГИДРОНАСОС',
                font=(font[0], 12),
                command = click_pump,
                **btn_master)
btn_cyl.grid(column=2, row=1)



main_window.mainloop()