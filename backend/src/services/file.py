import logging

from backend.src.models import File
from backend.src.repositories.file import FileRepository
from backend.src.schemas import IFileCreateSchema
from backend.src.services.base import BaseService


# Game Game Game Game Game Game

logger: logging.Logger = logging.getLogger(__name__)


class FileService(BaseService[FileRepository]):
    def __init__(self, repo: FileRepository) -> None:
        self.repo = repo

    async def new(self, file_obj: IFileCreateSchema) -> File:
        # file_obj = IFileCreateSchema(name="subreddit")
        instance = await self.repo.create(file_obj)
        # logger.info(f"New r/{subreddit.display_name} Game[{instance.ref_id}]")

        return instance
