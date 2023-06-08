from sqlmodel import Session, select
from models import File
from schemas import IFileUpdateSchema
from db.session import engine
#from repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

#class FileRepository(BaseRepository):
class FileRepository():
    _model = File
    @classmethod
    async def update_file(self, file_id:int, file:IFileUpdateSchema):
            with AsyncSession(engine) as session:
                db_file = await session.get(self._model, file_id)
                if not db_file:
                    print("File not_not found")
                    #raise HTTPException(status_code=404, detail="Hero not found")
                file_data = file.dict(exclude_unset=True)
                for key, value in file_data.items():
                    setattr(db_file, key, value)
                session.add(db_file)
                await session.commit()
                await session.refresh(db_file)
            return db_file



class SelectFiles():
    #session=sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    @classmethod
    async def all(cls) -> None:
        async with  AsyncSession(engine) as session:
            coroutine_files = await session.execute(select(File.id, File.name))
            files= coroutine_files.all()
            print(' files ----', files)
            return files
    @classmethod
    async def list_id_name_from_user_id(cls):
        async with  AsyncSession(engine) as session:
            coroutine_files = await session.execute(select(File.id, File.name).where(File.user_id==1))
            files = coroutine_files.all()
            print(' files ----', files)
            return files

