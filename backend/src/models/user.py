from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, text
import uuid as uuid_pkg

from backend.src.models.base import BaseModel


if TYPE_CHECKING:
    from backend.src.models.directories import Directory
    from backend.src.models.files import File


class User(BaseModel, table=True):
    name: str = Field(default=None, unique=True)
    ref_id: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        index=True,
        nullable=False,
        sa_column_kwargs={"default": text("gen_random_uuid()"), "unique": True},# "server_default"
    )
    directories: Optional[List["Directory"]] = Relationship(back_populates="user")
    files: Optional[List["File"]] = Relationship(back_populates="user")