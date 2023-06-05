import asyncio
from tkinter import Tk
from init_db import *
#from sqlmodel import Session
from db.session import engine
import tkinter as tk
from repositories.my__init__ import SelectFiles
from repositories.my__init__ import FileRepository

font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')

metadata_={}
#metadata_={'config': {'direction': 'p1', 'arrangement': 'vertical movement'}, 'm': 25.0, 'a': 1.0, 'P1': 270.0}
#_________________________SelectFiles_________________________________________________


def select_dir_of_user():
    with Session(engine) as session:
        directories = session.exec(select(Directory.name).where(File.user_id==1)).all()
        print(' directories ----', directories)
        return directories

def get_metadata_from_file(file_id):
    def _get_metadata():
        with Session(engine) as session:
            _metadata = session.exec(select(File.meta_data).where(col(File.id) == file_id)).first()
            print('meta___data2222_________________', _metadata)
        #window_.destroy()
        return _metadata
    return _get_metadata
# ------------------for file_id_input------------------------------------------
file_id=None
# -----------------------------------------------------------------------------
#list_files = select_file_of_user()
init_list_files = SelectFiles.all()
#list_files = SelectFiles.list_id_name_from_user_id()
# ---------------------------------------------------
def get_id_from_file(_file_id):

    def _get_id():
        global file_id
        file_id = _file_id
        print('def get_id_from_file(file_id):________________________', file_id)
        #window_.destroy()
        return file_id
    return _get_id
# ---------------------------------------------------
def file_id_input():
    global file_id

    window_ = tk.Tk()
    var=tk.IntVar()

    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window_.title(title_text)
    tk.Label(window_, text = lbl_text_message, font = (font[0],12)).grid(row = 0)
    lbl_error = tk.Label(window_, text=lbl_text_error, font=(font[0], 12), **btn_master)

    _row = 2
    for id, name in init_list_files:
        _row+=_row
        print('list_files___________________________________', init_list_files)
        tk.Button(window_,
                  text=name,
                  command=get_id_from_file(_file_id=id),
                  **btn_master).grid(column=0, row=_row)
    tk.Button(window_,
              text='ОТКРЫТЬ',
              command=lambda :window_.destroy(),
              **btn_master).grid(column=0, row=1000)
    print('_id_id_id_id_id_id1111-------------------------', file_id)
    window_.mainloop()
    print('_id_id_id_id_id_id2222-------------------------', file_id)
    return file_id
#-----------------------end-------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#--------------------------------w_metadata_to_file------------------------------------------------------------
#________________________updade file___________________________________________________
from schemas import IFileUpdateSchema


def update_file(file_id:int):
    _model=File
    def _update(file:IFileUpdateSchema) -> IFileUpdateSchema:
        with Session(engine) as session:
            db_file = session.get(_model, file_id)
            if not db_file:
                print("File not_not found")
                #raise HTTPException(status_code=404, detail="Hero not found")
            file_data = file.dict(exclude_unset=True)
            for key, value in file_data.items():
                setattr(db_file, key, value)
            session.add(db_file)
            session.commit()
            session.refresh(db_file)
        return db_file
    return _update




async def main() ->None:
    #metadata=get_metadata_from_file(1)()
    #print('metadata=get_metadata_from_file(1)\n', metadata)
    id_=None
    id_=file_id_input()
    r_from_file_func = get_metadata_from_file(file_id=id_)
    metadata=r_from_file_func()
    print('metadata_metadata_------------\n', metadata)

    #w_metadata_to_file_func=update_file(file_id=id_)
    w_metadata_to_file_func=FileRepository.update_file(file_id=id_)
    metadata["app"] = "w_metadata_to_file_func"
    #metadata.pop('app')

    w_metadata_to_file_func(file=IFileUpdateSchema(meta_data=metadata))



    #SelectFiles.list_id_name_from_user_id()

if __name__=='__main__':
    asyncio.run(main())