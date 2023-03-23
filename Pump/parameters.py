from pathlib import Path
from utils.parameters import file_name_input, r_from_file_to_metadata,\
                            w_metadata_to_file, parameter_input

metadata_pump = {}

name_par_pump = {
    "V": 'V (см3)- рабочий объём',
    "n": "n (об/мин)- скорость вращения ",
    "Q": "Q (л/мин)- требуемая подача",
    "M": 'M (даН*м ) - (деканьютон*м)вращающий момент ведомого вала',
    "P": 'P (кВт) - мощность  ведомого вала',
    "p": 'p (Bar) - давление (перепад давления)',
}


initial_dir_mot = str(Path(Path.cwd(), 'Pump', 'JsonFiles'))
#открываю или создаю файл для хранения параметров
file_name_pump = file_name_input(initial_dir_mot, metadata= metadata_pump)



# экземпляр функции r_from_file_to_metadata
r_from_file_pump = r_from_file_to_metadata(path_file=file_name_pump)


#переопределяю переменную-получаю словарь с внешнего файла
metadata_pump = r_from_file_pump()

# экземпляр функции w_metadata_to_file
w_to_file_pump = w_metadata_to_file(path_file=file_name_pump, metadata= metadata_pump)

parameter_pump_input = parameter_input(metadata = metadata_pump,
                                    _name_par = name_par_pump,
                                    _func_write = w_to_file_pump
                                    )