from sqlmodel import Session, select
from models import File
from schemas import IFileUpdateSchema
from db.session import engine
from repositories.base import BaseRepository


class FileRepository(BaseRepository):
    _model = File
    @classmethod
    def update_file(self, file_id:int):
        def _update(file:IFileUpdateSchema):
            with Session(engine) as session:
                db_file = session.get(self._model, file_id)
                if not db_file:
                    print("File not_not found")
                    #raise HTTPException(status_code=404, detail="Hero not found")
                file_data = file.dict(exclude_unset=True)
                for key, value in file_data.items():
                    setattr(db_file, key, value)
                session.add(db_file)
                session.commit()
                session.refresh(db_file)
            return db_file
        return _update


class SelectFiles():
    session = Session(engine)
    @classmethod
    def all(cls):
        with  cls.session:
            files = cls.session.exec(select(File.id, File.name)).all()
            print(' files ----', files)
            return files
    @classmethod
    def list_id_name_from_user_id(cls):
        with cls.session:
            files = cls.session.exec(select(File.id, File.name).where(File.user_id==1)).all()
            print(' files ----', files)
            return files