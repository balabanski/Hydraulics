from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import models
from backend.src.api import deps
from backend.src.repositories import FileRepository
from backend.src.schemas.file import IFileCreateSchema, IFileReadSchema, IFileUpdateSchema


# from starlette import status

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
    repo = FileRepository(db=session)
    # columns = ["id", "name"]
    # list_models_Files = await repo.all(sort_order="desc", select_columns=columns)
    # print("%%%%%%%%%%******list_models_Files_________\n", list_models_Files)
    # return list_models_Files
    list_models_Files = await repo.f(user_id=user.id)
    list_id_name = []
    for i in list_models_Files:
        list_id_name.append((i.id, i.name))

    return list_id_name


@router.post(
    "/create",
    response_description="create new file",
    response_model=IFileReadSchema,
)
async def create_file(
    name: str,
    session: AsyncSession = Depends(deps.get_db),
    user: models.User = Depends(deps.get_current_active_user),
):
    repo = FileRepository(db=session)
    obj_in = IFileCreateSchema(name=name, user_id=user.id)
    file = await repo.create(obj_in=obj_in)
    # try:
    #     scalar = await repo.get(user_id=user.id, name=name)
    #     if not scalar:
    #         # raise ObjectNotFound(f"Object with [{kwargs}] not found.")
    #         raise HTTPException(status_code=404, detail=f"Object with name [{name}] not found.")
    #     return scalar
    # except MultipleResultsFound as e:
    #     print("*************MultipleResultsFound")
    #     print(f"{e.args}".center(110, "*"))
    #     print(f"The file with name [{name}] already exists in the system")
    #     raise HTTPException(status_code=400, detail=f"The file with name [{name}] already exists in the system"
    return file  # ==>dict


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
