from sqlmodel import SQLModel
from typing import Optional, Dict
from pydantic import Field
from models.files import FileBase, File


class IFileUpdateSchema(FileBase):
    name: Optional[str]=None
    meta_data: Dict


class IFileCreateSchema(FileBase):
    pass


class IFileReadSchema:
    pass