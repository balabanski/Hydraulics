from typing import TYPE_CHECKING, Dict, Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from backend.src.models.base import BaseModel
from backend.src.models.directories import Directory
from backend.src.models.user import User


if TYPE_CHECKING:
    from backend.src.models.directories import Directory
    from backend.src.models.user import User


class FileBase(SQLModel):
    name: str = Field(index=True)
    # решение для data https://stackoverflow.com/questions/70567929/how-to-use-json-columns-with-sqlmodel
    meta_data: Dict = Field(default={}, sa_column=Column(JSON))
    directory_id: Optional[int] = Field(
        foreign_key="directory.id", description="The database id of the folders"
    )
    user_id: Optional[int] = Field(foreign_key="user.id", description="The database id of the user")


class File(BaseModel, FileBase, table=True):
    class Config:
        arbitrary_types_allowed = True

    user: Optional[User] = Relationship(back_populates="files")
    directory: Optional[Directory] = Relationship(back_populates="files")
