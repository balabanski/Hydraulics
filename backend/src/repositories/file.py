from typing import Optional

from backend.src.db.session import get_session
from backend.src.models import File
from backend.src.schemas import IFileUpdateSchema, IFileCreateSchema
from backend.src.repositories.sqlalchemy_ import BaseSQLAlchemyRepository

from sqlalchemy.ext.asyncio import AsyncSession

import logging

logger: logging.Logger = logging.getLogger(__name__)


class FileRepository(BaseSQLAlchemyRepository[File, IFileCreateSchema, IFileUpdateSchema]):
    _model = File

    # def __init__(self, db: AsyncSession) -> None:
    #     self.db = db
    #
    # async def create(self, obj_in: IFileCreateSchema) -> File:
    #
    #     db_obj = File(
    #         name=obj_in.name
    #     )
    #     print('db_obj = File(name=obj_in.name)_____________________________________________________', db_obj)
    #     self.db.add(db_obj)
    #     print('db.add(db_obj))__________________OK___________________________________')
    #     await self.db.commit()
    #     print('db.commit()__________________OK___________________________________')
    #     await self.db.refresh(db_obj)
    #     print('db.refresh(db_obj)__________________OK___________________________________')
    #     print('db_obj___________________________________________________________', db_obj)
    #     return db_obj


# repo = FileRepository(db=asyncio.run(get_session()))


# _________________________________________________for asyncio.run (использую)______________________________________


async def select_file(columns=["id", "name"]):
    repo = FileRepository(db=await get_session())
    list_id_name = await repo.all(sort_order="desc", select_columns=columns)
    print("await repo.all()___________________________", list_id_name)
    return list_id_name
    # response.headers["x-content-range"] = f"{len(games)}/{limit}"


"""


async def select_file() -> None:
    async with AsyncSession(engine) as session:
        coroutine_files = await session.execute(select(File.id, File.name))
        files = coroutine_files.all()
        print(' files ----', files)
    return files
"""


async def get_metadata_from_file(file_id):
    repo = FileRepository(db=await get_session())
    list_model_from_id = await repo.f(id=file_id)
    return list_model_from_id[0].meta_data


"""


async def get_metadata_from_file(file_id):
    async with AsyncSession(engine) as session:
        _metadata = await session.execute(select(File.meta_data).where(col(File.id) == file_id))
        metadata = _metadata.first()
        print('meta___data_____________________________', metadata)
        # window_.destroy()
        if metadata:
            return metadata[0]

"""


async def create_file(file: IFileCreateSchema):
    repo = FileRepository(db=await get_session())
    await repo.create(obj_in=file)
    # logger.info(f"Inserting new object________________[{file.__class__.__name__}]")


"""


async def create_file(file: IFileCreateSchema):
    logger.info(f"Inserting new object________________[{file.__class__.__name__}]")
    async with SessionLocal() as session:
        new_file = File(name=file.name, user_id=file.user_id, directory_id=file.directory_id, meta_data=file.meta_data)
        session.add(new_file)
        await session.commit()
    print("new_file.id______________________________________________", new_file.id)
    return new_file.id
"""


async def update_file(file_id: int, file: IFileUpdateSchema = None):
    repo = FileRepository(db=await get_session())
    file_current: Optional[File] = await repo.get(**{"id": file_id})
    print(
        "obj_current:Optional[File] = await repo.get('id'), _________________________________________",
        file_current,
    )
    await repo.update(obj_current=file_current, obj_in=file)


"""


async def update_file(file_id: int, file: IFileUpdateSchema = None):
    async with AsyncSession(engine) as session:
        db_file = await session.get(File, file_id)
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
"""


async def delete_file(file_id: int):
    repo = FileRepository(db=await get_session())
    await repo.delete(id=file_id)


"""


async def delete_file(file_id: int):
    async with AsyncSession(engine) as session:
        file = await session.get(File, file_id)
        if not file:
            print("File not_not found")
            #raise HTTPException(status_code=404, detail="Hero not found")
        await session.delete(file)
        await session.commit()
    return {"ok": True}
"""
# ________________________не использую_______________________________________________________________


# ___________________________________________________________BaseService____________________________________
from typing import Generic, TypeVar

from backend.src.interfaces.repository import IRepository


T = TypeVar("T", bound=IRepository)


class BaseService(Generic[T]):
    def __init__(self, repo: T) -> None:
        self.repo = repo


# _________________________________________________________________FileService_____________________________
import logging

logger: logging.Logger = logging.getLogger(__name__)


class FileService(BaseService[FileRepository]):
    def __init__(self, repo: FileRepository) -> None:
        self.repo = repo
