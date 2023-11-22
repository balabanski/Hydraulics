from typing import Optional, Dict
from backend.src.models.files import FileBase

from pydantic import BaseModel
from sqlmodel import SQLModel


class IFileUpdateSchema(FileBase):
    name: Optional[str] = None
    meta_data: Dict


class IFileCreateSchema(FileBase):
    pass


class IFileReadSchema(BaseModel):
    id: int
    name: str

    # class Config:
    #     orm_mode = True
