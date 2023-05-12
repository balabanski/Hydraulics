#from  .base import BaseModel
#from  .directories import Directory
#from .files import File
#from .user import User

import asyncio
import logging
from typing import Optional, List, Dict
from sqlmodel import Field, SQLModel, Column, DateTime, Session, Relationship, text, JSON, select, update, col, or_
import uuid as uuid_pkg
from datetime import datetime
from sqlalchemy.sql import func






from db.session import SessionLocal




logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)
class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    #create_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True),default = datetime.utcnow))
    create_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True),
                                                           server_default=func.now(),
                                                           nullable=True)
                                          )

    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True),
                                                            onupdate=func.now(),
                                                            nullable=True)

                                           )


class User(BaseModel, table=True):
    name: str = Field(default=None, unique=True)
    ref_id: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        index=True,
        nullable=False,
        sa_column_kwargs={"default": text("gen_random_uuid()"), "unique": True},# "server_default"
    )
    directories:Optional[List["Directory"]]=Relationship(back_populates="user")
    files: Optional[List["File"]]=Relationship(back_populates="user")


class Directory(BaseModel, table=True):
    name: str = Field(default=None, index=True)
    user_id:int = Field(default=None, foreign_key="user.id", description="The database id of the user")
    user:Optional[User]=Relationship(back_populates="directories")
    files:Optional[List["File"]]=Relationship(back_populates="directory")


class File(BaseModel, table=True):
    name: str = Field(default=None, index=True)
    # решение для data https://stackoverflow.com/questions/70567929/how-to-use-json-columns-with-sqlmodel
    meta_data: Dict = Field(default={}, sa_column=Column(JSON))
    class Config:
        arbitrary_types_allowed = True
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", description="The database id of the user")
    directory_id: Optional[int]=Field(default=None, foreign_key="directory.id", description="The database id of the folders")
    user: Optional[User] = Relationship(back_populates="files")
    directory:Optional[Directory]= Relationship(back_populates="files")