from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship
from backend.src.models.base import BaseModel

from backend.src.models.user import User

if TYPE_CHECKING:
    from backend.src.models.user import User
    from backend.src.models.files import File


class Directory(BaseModel, table=True):
    name: str = Field(default=None, index=True)
    user_id: int = Field(
        default=None, foreign_key="user.id", description="The database id of the user"
    )
    user: Optional[User] = Relationship(back_populates="directories")
    files: Optional[List["File"]] = Relationship(back_populates="directory")
