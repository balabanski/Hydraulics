from models import *
from db.session import engine

#-----------------------------create_db_and_tables---------------------------------------------
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




#---------------------------------select_dir_and_file----------------------------------------------
async def select_dir_and_file() -> None:
    with Session(engine) as session:
        results = session.exec(select(Directory.name, File.name).where(File.directory).where(User.id==1)).all()

        print(results)

async def select_file() -> None:
    pass

async def get_metadata_from_db(name_file) -> None:
    with Session(engine) as session:
        try:
            file_id = session.exec(select(File.id).where(col(File.name) == name_file)).one()
            print('file_id------------------------', file_id)
        except:
            print('ошибочка вышла: нет такого файла или их больше одного')
        results = session.exec(select(File.meta_data).where(col(File.id) == file_id)).first()
        print(results)


#________________________updade file___________________________________________________
class FileUpdate(SQLModel):
    name: Optional[str]=None
    meta_data: Optional[Dict]=None
    user_id: Optional[int] = None
    directory_id: Optional[int] = Field(default=None)


def update_file(file_id: int, file:FileUpdate):
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


#_________________________create user_________________________________________________
def create_user(name: str):
    with Session(engine) as session:
        user = User(name=name)
        session.add(user)
        session.commit()

#_________________________create file_________________________________________________
def create_file(name: str, user_id=None, directory_id=None):
    with Session(engine) as session:
        file = File(name=name, user_id =user_id, directory_id=directory_id)
        session.add(file)
        session.commit()

#________________________updade file___________________________________________________
class FileUpdate(SQLModel):
    name: Optional[str]=None
    meta_data: Optional[Dict]=None
    user_id: Optional[int] = None
    directory_id: Optional[int] = Field(default=None)


def update_file(file_id: int, file:FileUpdate):
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

#____________________________create file in directory____________________________________________________________
def create_file_in_directory(file: File):
    with Session(engine) as session:
        db_file = session.add(file)
        file_data=file.dict()
        print('file_data______________', file_data)
        session.commit()

        print('db_file________', db_file, 'type(db_file)_________', type(db_file))
        return db_file


#___________________________delete file_______________________________________________________________________
def delete_file(file_id: int):
    with Session(engine) as session:
        file = session.get(File, file_id)
        if not file:
            print("File not_not found")
            #raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(file)
        session.commit()
        return {"ok": True}


async def main() -> None:
    #logger.info("Creating initial data")
    #create_db_and_tables()
    #await create_init_data()
    #await select_dir_and_file()
    #await get_metadata_from_db(name_file= "Prestel_main")
    update_file(6,FileUpdate(meta_data={'value': 'Petiusha'}))
    #create_file_in_directory(File(name='cyl_for Sacha', directory_id=2, meta_data={'p1':250}))
    #create_user("Petya")
    #create_file('file_userPetya', 2)
    #delete_file(9)

    #logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
