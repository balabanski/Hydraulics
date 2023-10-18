from typing import Optional, Dict
from backend.src.models.files import FileBase


class IFileUpdateSchema(FileBase):
    name: Optional[str] = None
    meta_data: Dict


class IFileCreateSchema(FileBase):
    pass


class IFileReadSchema:
    pass