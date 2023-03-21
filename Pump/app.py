from Pump.parameters import file_name_pump, w_to_file_pump, metadata_pump
from Pump.pump import _V, _Q, _P
import tkinter as tk
import json
from utils.parameters import font, btn_master
from utils._app import get_all_parameters



main_window_pump = tk.Tk()
main_window_pump.title('расчет параметров гидромотора')

get_all_parameters_pump= get_all_parameters(main_window = main_window_pump,
                                           file_name = file_name_pump,
                                           metadata = metadata_pump,
                                           func_w_to_file = w_to_file_pump,)

get_all_parameters_pump()




main_window_pump.mainloop()