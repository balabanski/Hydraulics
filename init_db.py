from models import *

from src.db.session import engine
from sqlmodel import SQLModel, select, Session

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import logging
logger: logging.Logger = logging.getLogger(__name__)


#-----------------------------create_db_and_tables---------------------------------------------
async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def async_session():
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    print('SessionLocal__________', SessionLocal)

    async with SessionLocal() as s:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        #yield s
        print('SessionLocal after yield__________', SessionLocal)
    '''
    async with engine.begin() as conn:
        #await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    '''
    await engine.dispose()

async def init_models():
    with engine.begin() as conn:
        #conn.run_sync(SQLModel.metadata.drop_all)
        conn.run_sync(SQLModel.metadata.create_all)

#asyncio.run(init_models())
#---------------------------------select_dir_and_file----------------------------------------------

async def select_dir_and_file() -> None:
    async with AsyncSession(engine) as session:
        _results = await session.execute(select(Directory.name, File.name).where(File.directory).where(User.id==1))
        results=_results.all()

        print('results------------------------------------------------------', results)
        return results


# --------------------------get_metadata_from_file-------------------------------------------

async def get_metadata(func, file_id):
    await func(file_id)


#________________________updade file___________________________________________________




#_________________________create user_________________________________________________
def create_user(name: str):
    with Session(engine) as session:
        user = User(name=name)
        session.add(user)
        session.commit()

#_________________________create file_________________________________________________
'''
async def create_file(name: str, user_id=None, directory_id=None):
    async with AsyncSession(engine) as session:
        file = File(name=name, user_id =user_id, directory_id=directory_id)
        session.add(file)
        await session.commit()
'''

'''
async def create_file(file: IFileCreateSchema):
    logger.info(f"Inserting new object[{file.__class__.__name__}]")
    async with AsyncSession(engine) as session:
        new_file=File(name=file.name, user_id=file.user_id,directory_id=file.directory_id, meta_data=file.meta_data)
        session.add(new_file)
        await session.commit()
'''


#___________________________delete file_______________________________________________________________________




async def main() -> None:
    logger.info("Creating initial data")

    #await delete_file(7)

    #await create_file(file=IFileCreateSchema(name="new_file"))

    #await FileRepository.update_file(2, file=IFileUpdateSchema(meta_data={'meta': 'update2'})) # НЕ РАБОТАЕТ
    #await update_file(2, file=IFileUpdateSchema(meta_data={'meta': 'update3'}))





if __name__ == "__main__":
    asyncio.run(main())
