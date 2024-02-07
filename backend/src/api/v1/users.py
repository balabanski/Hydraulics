from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src import repositories, models, schemas
from backend.src.api import deps
from backend.src.core.config import settings
from backend.src.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    repo = repositories.UserRepository(db=db)
    users = await repo.all(skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    repo = repositories.UserRepository(db=db)
    user = await repo.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await repo.create(obj_in=user_in)

    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.hashed_password
        )
    return user


@router.put("/update-me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    obj_in: schemas.UserUpdate,
    # password: str = Body(None),
    # full_name: str = Body(None),
    # email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    repo = repositories.UserRepository(db=db)
    print('*****in rout update_my*********obj_in: schemas.UserUpdate****************************************\n',
          obj_in)
    print('*****in rout update_my*********current_user: models.User = Depends(deps.get_current_active_user)**\n',
          current_user)
    # current_user_data = jsonable_encoder(current_user)  # dict
    # print('*****in rout update_my*********current_user_data = jsonable_encoder(current_user)*********\n',
    #       current_user_data)
    # user_in = schemas.UserUpdate(**current_user_data)
    # if password is not None:
    #     user_in.password = password
    # if full_name is not None:
    #     user_in.full_name = full_name
    # if email is not None:
    #     user_in.email = email
    user = await repo.update(obj_current=current_user, obj_in=obj_in)
    return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/create-user-open", response_model=schemas.User)
async def create_user_open(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_create: schemas.UserCreate = Body(..., embed=True, alias='user'),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    repo = repositories.UserRepository(db=db)
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = await repo.get_by_email(email=user_create.email)  # None

    if user is not None:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = await repo.create(user_create)
    # user_in = user_create.dict()
    # print("in API:**** user_in**** = user_create.dict()______________dict_______________", user_in)
    # user = await repo.create(**user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    repo = repositories.UserRepository(db=db)
    user = await repo.get(id=user_id)
    if user == current_user:
        return user
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user (for a superuser).
    """
    repo = repositories.UserRepository(db=db)
    user = await repo.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await repo.update(obj_current=user, obj_in=user_in)
    return user
