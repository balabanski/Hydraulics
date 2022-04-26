
from Cylinder.cylinder import * #F1, F2, F_ring, F_circle
from Cylinder.parameters import c, messages, r_file, get_par, file_name
import tkinter as tk


font =['Arial Bold']


window = tk.Tk()
window.title("Расчет параметров цилиндра")


txt_param =tk.Text(width=30, height=12, font = (font[0], 15))
txt_param.grid(column = 1, row = 0)
def get_param():
    #file_name = fd.askopenfilename()
    with open(file_name, 'r') as file:
        c_read = file.read()
    txt_param.insert(1.0, c_read)
b1 = tk.Button(text="Все параметры", command= get_param)
b1.grid(column = 0, row = 0)


btn_1 = tk.Button(window, text = 'расчет {}'.format(messages['F1']), font = (font[0], 15))
btn_1.grid(column = 0, row = 1)
lbl_1 = tk.Label(window, text = 'результат',font = (font[0], 15) )
lbl_1.grid(column = 1, row = 1)
def clicked_1():
    lbl_1.configure(text = F1())
    lbl_2.configure(text = F_ring(c['d1'],c['d2']))
btn_1['command'] = clicked_1

btn_2 = tk.Button(window, text = '{}'.format(messages['F2']), font = (font[0], 15))
btn_2.grid(column = 0, row = 2)
lbl_2 = tk.Label(window, text = 'результат',font = (font[0], 15) )
lbl_2.grid(column = 1, row = 2)
def clicked_2():
    lbl_2.configure(text = F2())
    lbl_1.configure(text = F_circle(c['d1']))
btn_2['command'] = clicked_2


window.mainloop()
