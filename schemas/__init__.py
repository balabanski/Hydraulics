from sqlmodel import SQLModel
from typing import Optional, Dict
from pydantic import Field


class FileUpdateSchema(SQLModel):
    name: Optional[str]=None
    meta_data: Optional[Dict]=None
    user_id: Optional[int] = None
    directory_id: Optional[int] = Field(default=None)