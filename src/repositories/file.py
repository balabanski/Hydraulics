from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, col

from src.db.session import engine, SessionLocal
from models import File
from src.schemas import IFileUpdateSchema, IFileCreateSchema
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository

import logging
logger: logging.Logger = logging.getLogger(__name__)


class FileRepository(BaseSQLAlchemyRepository[File, IFileCreateSchema, IFileUpdateSchema]):
    _model = File


async def update_file(file_id: int, file: IFileUpdateSchema = None):
    async with AsyncSession(engine) as session:
        print('!!!!!!!!!!!!!СИГНАЛ________update_file!!!!!!!!!!!!!!!!!!!!!!')
        db_file = await session.get(File, file_id)
        if not db_file:
            print("File not_not found")
            #raise HTTPException(status_code=404, detail="Hero not found")
        file_data = file.dict(exclude_unset=True)
        print('!!!!!!!!!file_data!!!!!!!!!!!____________________', file_data)
        for key, value in file_data.items():
            setattr(db_file, key, value)
        session.add(db_file)
        await session.commit()
        await session.refresh(db_file)
        return db_file


async def get_metadata_from_file(file_id):
    async with AsyncSession(engine) as session:
        _metadata = await session.execute(select(File.meta_data).where(col(File.id) == file_id))
        metadata = _metadata.first()
        print('meta___data_________________', metadata)
    #window_.destroy()
    return metadata


class SelectFiles:
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


async def select_file() -> None:
    async with  AsyncSession(engine) as session:
        coroutine_files = await session.execute(select(File.id, File.name))
        files = coroutine_files.all()
        print(' files ----', files)
        return files


async def create_file(file: IFileCreateSchema):
    logger.info(f"Inserting new object________________[{file.__class__.__name__}]")
    async with SessionLocal() as session:
        new_file=File(name=file.name, user_id=file.user_id,directory_id=file.directory_id, meta_data=file.meta_data)
        session.add(new_file)
        await session.commit()


async def delete_file(file_id: int):
    async with AsyncSession(engine) as session:
        file = await session.get(File, file_id)
        if not file:
            print("File not_not found")
            #raise HTTPException(status_code=404, detail="Hero not found")
        await session.delete(file)
        await session.commit()
        return {"ok": True}