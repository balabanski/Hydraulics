from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlmodel import select

from backend.src.core.security import get_password_hash, verify_password
from backend.src.repositories.sqlalchemy_ import BaseSQLAlchemyRepository
from backend.src.models.user import User
from backend.src.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseSQLAlchemyRepository[User, UserCreate, UserUpdate]):
    _model = User

    async def get_by_email(self, *, email: str) -> Optional[User]:
        # logger.info(f"******Fetching [{self._model.__table__.name.capitalize()}] object by [{kwargs}]")  # type: ignore
        return await self.get(email=email)

    async def authenticate(self,  *, email: str, password: str) -> Optional[User]:
        user_ = await self.get(email=email)
        if not user_:
            return None
        if not verify_password(password, user_.hashed_password):
            return None
        return user_

    # async def create(self, **obj_in) -> User:
    #     db_obj = User(**obj_in)
    #     self.db.add(db_obj)
    #     await self.db.commit()
    #     await self.db.refresh(db_obj)
    #     return db_obj

    # async def update(
    #     self,  *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if update_data["password"]:
    #         hashed_password = get_password_hash(update_data["password"])
    #         del update_data["password"]
    #         update_data["hashed_password"] = hashed_password
    #     return super().update(obj_current=db_obj, obj_in=update_data)

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_repo = UserRepository(User)
