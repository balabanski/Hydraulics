from models import File
from schemas import IFileUpdateSchema, IFileCreateSchema
from repositories.sqlalchemy import BaseSQLAlchemyRepository



class FileRepository(BaseSQLAlchemyRepository[File, IFileCreateSchema, IFileUpdateSchema]):
    _model = File

