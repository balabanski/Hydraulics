from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import models
from backend.src.api import deps
from backend.src.repositories import FileRepository
from backend.src.schemas.file import IFileCreateSchema, IFileReadSchema, IFileUpdateSchema


router = APIRouter()


@router.get(
    "/list files",
    response_description="List all files instances",
    response_model=List[Tuple],
)
async def list_files(
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    # columns = ["id", "name"]
    repo = FileRepository(db=session)
    # list_models_Files = await repo.all(sort_order="desc", select_columns=columns)
    list_models_Files = await repo.f(user_id=user.id)
    list_id_name = []
    for i in list_models_Files:
        list_id_name.append((i.id, i.name))

    return list_id_name


@router.post(
    "/create",
    response_description="create new file",
    response_model=List[IFileReadSchema],
)
async def create_file(
    name: str,
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    repo = FileRepository(db=session)
    file = IFileCreateSchema(name=name, user_id=user.id)
    await repo.create(obj_in=file)
    list_id_name = await repo.f(user_id=user.id)
    return list_id_name


@router.post(
    "/delete",
    response_description="delete file",
    response_model=List[IFileReadSchema],
)
async def delete_file(
    file_id: int,
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    repo = FileRepository(db=session)
    await repo.delete(id=file_id)

    list_id_name = await repo.f(user_id=user.id)
    return list_id_name


@router.get(
    "/get metadata",
    response_description="metadata of file",
    response_model=Dict,
)
async def get_metadata(
    file_id: int,
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    repo = FileRepository(db=session)
    list_model_from_id = await repo.f(id=file_id)
    return list_model_from_id[0].meta_data


@router.post(
    "/update",
    response_description="update file",
    # response_model=Dict,
)
async def update_file(
    file_id: int,
    obj_in: IFileUpdateSchema,
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    repo = FileRepository(db=session)

    await repo.update(file_id=file_id, file=obj_in)
    list_model_from_id = await repo.f(id=file_id)
    return list_model_from_id[0]
