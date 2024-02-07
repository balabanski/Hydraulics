# from web_app.utils.parameters import font, btn_master
from web_app.utils.settings_gui import font, btn_master
import tkinter as tk
import json
from web_app.requests.req_file import update_file


def get_all_parameters(main_window=None,
                       file_id=None,
                       metadata=None,
                       file_name=None
                       ):
    def _get_all_parameters():
        txt_param = tk.Text(main_window, width=50, height=12, font=(font[0], 12))
        txt_param.grid(column=0, row=1)

        error_open_file_message = '\nне задан файл для хранения параметров\n'

        def get_all_param():
            txt_param.delete(0.0, 100.100)
            if file_id:
                c_read = json.dumps(metadata, sort_keys=True, indent=4)
                txt_param.insert(0.0, c_read)
            else:
                txt_param.insert(0.0, error_open_file_message)

        if file_id:
            txt_param.insert(0.0, '\nпараметры загружены \n для просмотра жми кнопку "параметры"\n')

        else:
            txt_param.insert(0.0, error_open_file_message)

        btn_all_parameters = tk.Button(main_window, text="Отобразить параметры", font=(font[0], 12),
                                       command=get_all_param, **btn_master)
        btn_all_parameters.grid(column=0, row=0)

        def change_param():
            try:
                new_param = txt_param.get(0.0, 100.100)
                _param = json.loads(new_param.replace("'", '"'))
                metadata.clear()
                for key, val in _param.items():
                    metadata[key] = val
                print('id_=file_id,, _______', file_id)
                print('name = file_name______________', file_name)
                print('meta_data=metadata____________________________\n',metadata)
                update_file(id_=file_id, name=file_name,  meta_data=metadata)
                get_all_param()
            except:
                txt_param.delete(0.0, 100.100)
                txt_param.insert(0.0, 'ошибка синтаксиса файла json(запятые, двоеточия)\n'
                                      'побробуйте еще')

        btn_change_parameters = tk.Button(main_window, text="Редактировать & сохранить", font=(font[0], 12),
                                          command=change_param, **btn_master)
        btn_change_parameters.grid(column=1, row=0)

    return _get_all_parameters
