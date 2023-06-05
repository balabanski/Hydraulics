
from typing import TYPE_CHECKING, Optional, List, Dict
from sqlmodel import Field, SQLModel, Column, DateTime, Session, Relationship, text, JSON, select, update, col, or_
from models.base import BaseModel

from models.user import User
if TYPE_CHECKING:
    from models.user import User
    from models.files import File

class Directory(BaseModel, table=True):
    name: str = Field(default=None, index=True)
    user_id:int = Field(default=None, foreign_key="user.id", description="The database id of the user")
    user:Optional[User]=Relationship(back_populates="directories")
    files:Optional[List["File"]]=Relationship(back_populates="directory")