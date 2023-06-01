from sqlalchemy.engine import Connection  # noqa

from sqlmodel import Session

#from app.helpers.exceptions import EntityDoesNotExist, GetReturnedMoreThatOneEntity
from resources import constants


class BaseRepository:
    _model = None

    def __init__(self, *, db: Session) -> None:
        self.db = db

    def save(self):
        self.db.add(self)
        self.db.commit()
        return self

    def commit(self):
        self.db.commit()

    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()
        return self

    def delete_all(self):
        self.filter().delete()
        self.db.commit()

    def create(self, **data):
        obj = self._model(**data)
        self.db.add(obj)
        self.db.commit()
        return obj

    def add(self, obj):
        self.db.add(obj)
        self.db.commit()

    def filter_by(self, **kwargs):
        return self.db.query(self._model).filter_by(**kwargs)

    def filter(self, *args, **kwargs):
        return self.db.query(self._model).filter(*args, **kwargs)

    def get_object_or_404(self, **data):
        _result = self.db.query(self._model).filter_by(**data)
        if _result.count() > 1:
            print(constants.MORE_THAN_ONE_INSTANCE_ERROR)
            #raise GetReturnedMoreThatOneEntity(constants.MORE_THAN_ONE_INSTANCE_ERROR)
        elif _result.count() == 0:
            print(constants.OBJECT_DOES_NOT_EXISTS)
            #raise EntityDoesNotExist(constants.OBJECT_DOES_NOT_EXISTS)
        return _result.first()

    def get_or_create(self, **kwargs):
        instance = self.db.query(self._model).filter_by(**kwargs).first()
        if instance:
            return instance, False
        instance = self._model(**kwargs)
        instance.save()
        return instance, True
