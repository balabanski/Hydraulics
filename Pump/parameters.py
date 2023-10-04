from utils.parameters import file_id_input, update_file, parameter_input
from src.repositories.file import get_metadata_from_file
import asyncio

metadata_pump = {}

name_par_pump = {
    "V": 'V (см3)- рабочий объём',
    "n": "n (об/мин)- скорость вращения ",
    "Q": "Q (л/мин)- требуемая подача",
    "M": 'M (даН*м ) - (деканьютон*м)вращающий момент ведомого вала',
    "P": 'P (кВт) - мощность  ведомого вала',
    "p": 'p (Bar) - давление (перепад давления)',
}

file_id = file_id_input()

# экземпляр функции r_from_file_to_metadata
# экземпляр функции r_from_file_to_metadata
r_from_file_func = get_metadata_from_file(file_id=file_id)  # coroutine object

# переопределяю переменную-получаю словарь с внешнего файла
metadata_pump = asyncio.run(r_from_file_func)

# экземпляр функции w_metadata_to_file
w_metadata_to_file_func = update_file(file_id=file_id)  # coroutyne

parameter_pump_input = parameter_input(metadata=metadata_pump,
                                       _name_par=name_par_pump,
                                       file_name=file_id,
                                       )
