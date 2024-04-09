import logging
# import uuid as uuid_pkg
from datetime import datetime
from typing import Optional

from sqlalchemy.sql import func
from sqlmodel import Column, DateTime, Field, SQLModel


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    # create_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True),default = datetime.utcnow))
    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    )
