from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Dict

from backend.src.repositories import FileRepository
from backend.src.api import deps
from backend.src.schemas.file import IFileReadSchema, IFileCreateSchema

router = APIRouter()


@router.get(
    "/list files",
    response_description="List all files instances",
    response_model=List[IFileReadSchema],
)
async def list_files(session: AsyncSession = Depends(deps.get_db)):
    columns = ["id", "name"]
    repo = FileRepository(db=session)
    list_id_name = await repo.all(sort_order="desc", select_columns=columns)
    print("await repo.all()___________________________", list_id_name)
    return list_id_name


@router.post(
    "/create",
    response_description="create new file",
    response_model=List[IFileReadSchema],
)
async def create_file(
        name: str,
        session: AsyncSession = Depends(deps.get_db),
):
    repo = FileRepository(db=session)
    file = IFileCreateSchema(name=name)
    await repo.create(obj_in=file)
    list_id_name = await repo.all(sort_order="desc", select_columns=["id", "name"])
    return list_id_name


@router.post(
    "/delete",
    response_description="delete file",
    response_model=List[IFileReadSchema],
)
async def delete_file(
        file_id: int,
        session: AsyncSession = Depends(deps.get_db),
):
    repo = FileRepository(db=session)
    await repo.delete(id=file_id)
    list_id_name = await repo.all(sort_order="desc", select_columns=["id", "name"])
    return list_id_name


@router.get(
    "/get metadata",
    response_description="metadata of file",
    response_model=Dict,
)
async def get_metadata(
        file_id: int,
        session: AsyncSession = Depends(deps.get_db),
):
    repo = FileRepository(db=session)
    list_model_from_id = await repo.f(id=file_id)
    return list_model_from_id[0].meta_data
