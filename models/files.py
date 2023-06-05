import logging
from typing import TYPE_CHECKING, Optional, List, Dict
from sqlmodel import Field, SQLModel, Column, DateTime, Session, Relationship, text, JSON, select, update, col, or_

from models.base import BaseModel
from models.user import User
from models.directories import Directory
if TYPE_CHECKING:
    from models.user import User
    from models.directories import Directory


class FileBase(SQLModel):
    name: str = Field(index=True)
    # решение для data https://stackoverflow.com/questions/70567929/how-to-use-json-columns-with-sqlmodel
    meta_data: Dict = Field(default={}, sa_column=Column(JSON))
    directory_id: Optional[int] = Field(default=None, foreign_key="directory.id",
                                        description="The database id of the folders")

class File(BaseModel, FileBase,table=True):
    class Config:
        arbitrary_types_allowed = True
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", description="The database id of the user")
    user: Optional[User] = Relationship(back_populates="files")
    directory:Optional[Directory]= Relationship(back_populates="files")