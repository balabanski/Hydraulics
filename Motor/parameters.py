from pathlib import Path
from utils.parameters import file_id_input, get_metadata_from_file,\
                            update_file, parameter_input

metadata_mot = {}

name_par_mot = {
    "V": 'V (см3)- рабочий объём',
    "n": "n (об/мин)- скорость вращения ",
    "Q": "Q (л/мин)- требуемая подача",
    "M": 'M (даН*м ) - (деканьютон*м)вращающий момент ведомого вала',
    "P": 'P (кВт) - мощность  ведомого вала',
    "p": 'p (Bar) - давление (перепад давления)',
}


initial_dir_mot = str(Path(Path.cwd(), 'Motor', 'JsonFiles'))
#открываю или создаю файл для хранения параметров
file_name_mot = file_id_input(initial_dir_mot, metadata= metadata_mot)



# экземпляр функции r_from_file_to_metadata
r_from_file_mot = get_metadata_from_file(path_file=file_name_mot)


#переопределяю переменную-получаю словарь с внешнего файла
metadata_mot = r_from_file_mot()

# экземпляр функции w_metadata_to_file
w_to_file_mot = update_file(path_file=file_name_mot)

parameter_mot_input = parameter_input(metadata = metadata_mot,
                                    _name_par = name_par_mot,
                                    _func_write = w_to_file_mot
                                    )