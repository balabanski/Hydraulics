from typing import Dict, Optional

# from pydantic import BaseModel
from backend.src.models.base import BaseModel
from backend.src.models.files import FileBase


class IFileUpdateSchema(FileBase):
    name: Optional[str]
    meta_data: Dict


class IFileCreateSchema(FileBase):
    pass


# class IFileReadSchema(BaseModel):
class IFileReadSchema(FileBase, BaseModel):
    pass

    # class Config:
    #     orm_mode = True
