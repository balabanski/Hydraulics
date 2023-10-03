from pathlib import Path
from utils.parameters import file_id_input,  update_file, parameter_input
from src.repositories.file import get_metadata_from_file
import asyncio

metadata_mot = {}


name_par_mot = {
    "V": 'V (см3)- рабочий объём',
    "n": "n (об/мин)- скорость вращения ",
    "Q": "Q (л/мин)- требуемая подача",
    "M": 'M (даН*м ) - (деканьютон*м)вращающий момент ведомого вала',
    "P": 'P (кВт) - мощность  ведомого вала',
    "p": 'p (Bar) - давление (перепад давления)',
}


file_id = file_id_input()

# экземпляр функции r_from_file_to_metadata
r_from_file_func = get_metadata_from_file(file_id=file_id)  # coroutine object

#переопределяю переменную-получаю словарь с внешнего файла
metadata_mot = asyncio.run(r_from_file_func)

# экземпляр функции w_metadata_to_file
w_metadata_to_file_func = update_file(file_id=file_id)  # coroutyne

parameter_mot_input = parameter_input(metadata = metadata_mot,
                                    _name_par = name_par_mot,
                                    file_name=file_id
                                    )