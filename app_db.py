import asyncio
from tkinter import Tk
from init_db import *
#from sqlmodel import Session
from db.session import engine
import tkinter as tk

font = ['Arial Bold']
btn_master = dict(bg='#000000', activebackground='#555555',
                  fg='#ffffff', activeforeground='#ffffff')

metadata_={}
#metadata_={'config': {'direction': 'p1', 'arrangement': 'vertical movement'}, 'm': 25.0, 'a': 1.0, 'P1': 270.0}
#_________________________SelectFiles_________________________________________________
class SelectFiles():
    session = Session(engine)
    @classmethod
    def all(cls):
        with  cls.session:
            files = cls.session.exec(select(File.id, File.name)).all()
            print(' files ----', files)
            return files
    @classmethod
    def list_id_name_from_user_id(cls):
        with cls.session:
            files = cls.session.exec(select(File.id, File.name).where(File.user_id==1)).all()
            print(' files ----', files)
            return files

def select_dir_of_user():
    with Session(engine) as session:
        directories = session.exec(select(Directory.name).where(File.user_id==1)).all()
        print(' directories ----', directories)
        return directories

def get_metadata_from_file(file_id):
    def _get_metadata():
        global _metadata
        with Session(engine) as session:
            _metadata = session.exec(select(File.meta_data).where(col(File.id) == file_id)).first()
            print('meta___data2222_________________', _metadata)
        #window_.destroy()
        return _metadata
    return _get_metadata
# ------------------for file_id_input------------------------------------------
_id=None
# -----------------------------------------------------------------------------
#list_files = select_file_of_user()
list_files = SelectFiles.all()
#list_files = SelectFiles.list_id_name_from_user_id()
# ---------------------------------------------------
def get_id_from_file(file_id):

    def _get_id():
        global _id
        _id = file_id
        print('def get_id_from_file(file_id):________________________', _id)
        #window_.destroy()
        return _id
    return _get_id
# ---------------------------------------------------
def file_id_input():
    global _id

    window_ = tk.Tk()
    var=tk.IntVar()

    title_text = 'открыть или создать файл для хранения параметров'
    lbl_text_error = 'Для работы необходимо ' + title_text
    lbl_text_message = lbl_text_error + '\nвыбери вариант'

    window_.title(title_text)
    tk.Label(window_, text = lbl_text_message, font = (font[0],12)).grid(row = 0)
    lbl_error = tk.Label(window_, text=lbl_text_error, font=(font[0], 12), **btn_master)

    _row = 2
    for id, name in list_files:
        _row+=_row
        print('list_files___________________________________', list_files)
        tk.Button(window_,
                  text=name,
                  command=get_id_from_file(file_id=id),
                  **btn_master).grid(column=0, row=_row)
    tk.Button(window_,
              text='ОТКРЫТЬ',
              command=lambda :window_.destroy(),
              **btn_master).grid(column=0, row=1000)
    print('_id_id_id_id_id_id1111-------------------------', _id)
    window_.mainloop()
    print('_id_id_id_id_id_id2222-------------------------', _id)
    return _id
#-----------------------end-------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#--------------------------------w_metadata_to_file------------------------------------------------------------
#________________________updade file___________________________________________________
class FileUpdate(SQLModel):
    name: Optional[str]=None
    meta_data: Optional[Dict]=None
    user_id: Optional[int] = None
    directory_id: Optional[int] = Field(default=None)


def w_metadata_to_file(file_id:int):
    def _update(file:FileUpdate):
        with Session(engine) as session:
            db_file = session.get(File, file_id)
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
    #metadata_=get_metadata_from_file(1)()
    #print('metadata_=get_metadata_from_file(1)\n', metadata_)
    __id=2
    __id=file_id_input()
    metadata_=get_metadata_from_file(file_id=__id)()
    print('metadata_metadata_------------\n', metadata_)

    new=w_metadata_to_file(file_id=__id)
    metadata_["app"] = "new"

    new(file=FileUpdate(meta_data=metadata_))



    #SelectFiles.list_id_name_from_user_id()

if __name__=='__main__':
    asyncio.run(main())