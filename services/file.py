import logging
from typing import Optional, Union
from uuid import UUID

from sqlmodel import select

from services.base import BaseService
from repositories.file import FileRepository

from models.files import File


from schemas.file import IFileCreateSchema

# Game Game Game Game Game Game

logger: logging.Logger = logging.getLogger(__name__)


class FileService(BaseService[FileRepository]):
    def __init__(self, repo: FileRepository) -> None:
        self.repo = repo
    async def new(self, file_obj:IFileCreateSchema) -> File:
        #file_obj = IFileCreateSchema(name="subreddit")
        instance = await self.repo.create(file_obj)
        #logger.info(f"New r/{subreddit.display_name} Game[{instance.ref_id}]")

        return instance




