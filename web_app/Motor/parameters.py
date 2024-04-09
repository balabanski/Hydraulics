from web_app.utils.parameters import gui_filedialog, parameter_input
from web_app.requests.req_file import get_metadata_from_file

name_par_mot = {
    "V": 'V (см3)- рабочий объём',
    "n": "n (об/мин)- скорость вращения ",
    "Q": "Q (л/мин)- требуемая подача",
    "M": 'M (даН*м ) - (деканьютон*м)вращающий момент ведомого вала',
    "P": 'P (кВт) - мощность  ведомого вала',
    "p": 'p (Bar) - давление (перепад давления)',
}

file_list = gui_filedialog()
file_id = file_list[0]
file_name = file_list[1]

metadata_mot = get_metadata_from_file(id_=file_id)


parameter_mot_input = parameter_input(metadata=metadata_mot,
                                      _name_par=name_par_mot,
                                      _file_id=file_id,
                                      _file_name=file_name
                                      )
