import logging
from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from backend.src.interfaces.repository import IRepository
from backend.src.repositories.enums import OrderEnum, SortEnum


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
logger: logging.Logger = logging.getLogger(__name__)


class BaseSQLAlchemyRepository(IRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _model: Type[ModelType]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        logger.info(f"\n**********Inserting new object[{obj_in.__class__.__name__}]")

        db_obj = self._model.from_orm(obj_in)

        kwargs = {}
        add = kwargs.get("add", True)
        flush = kwargs.get("flush", True)
        commit = kwargs.get("commit", True)
        # async with self.db:
        if add:
            self.db.add(db_obj)
            # Navigate these with caution
        if add and commit:
            try:
                await self.db.commit()
                await self.db.refresh(db_obj)
            except Exception as exc:
                logger.error(exc)
                await self.db.rollback()

        elif add and flush:
            await self.db.flush()
        return db_obj

    async def get(self, **kwargs: Any) -> Optional[ModelType]:
        logger.info(
            f"\n**********Fetching one_or_none[{self._model.__table__.name.capitalize()}] object by [{kwargs}]"
        )  # type: ignore

        query = select(self._model).filter_by(**kwargs)
        async with self.db:
            response = await self.db.execute(query)
            scalar: Optional[ModelType] = response.scalar_one_or_none()

        if not scalar:
            # raise ObjectNotFound(f"Object with [{kwargs}] not found.")
            raise HTTPException(status_code=404, detail=f"Object with [{kwargs}] not found.")

        return scalar

    async def f(self, **kwargs: Any) -> List[ModelType]:
        logger.info(
            f"\n**********Filtering all [{self._model.__table__.name.capitalize()}] object by [{kwargs}]"
        )  # type: ignore
        async with self.db:
            query = select(self._model).filter_by(**kwargs)
            response = await self.db.execute(query)

        scalars: List[ModelType] = response.scalars().all()

        return scalars

    async def update(self, obj_current: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        logger.info(
            f"\n**********Updating [{self._model.__table__.name.capitalize()}] object with [{obj_in}]"
        )  # type: ignore

        update_data = obj_in.dict(
            exclude_unset=True
        )  # This tells Pydantic to not include the values that were not sent

        for field in update_data:
            setattr(obj_current, field, update_data[field])

        async with self.db:
            self.db.add(obj_current)
            await self.db.commit()
            await self.db.refresh(obj_current)

        return obj_current

    async def delete(self, **kwargs: Any) -> None:
        logger.info(
            f"\n**********Deleting [{self._model.__table__.name.capitalize()}] object by [{kwargs}]"
        )  # type: ignore
        async with self.db:
            obj = await self.get(**kwargs)

            await self.db.delete(obj)
            await self.db.commit()

    async def all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        select_columns: Optional[List[str]] = None,
    ) -> List[ModelType]:
        logger.info(f"********Fetching all objects by[{self._model.__table__.name.capitalize()}]")  # type: ignore
        columns = self._model.__table__.columns  # type: ignore

        if not sort_field:
            sort_field = SortEnum.CREATED_AT
        if not sort_order:
            sort_order = OrderEnum.DESC

        order_by = getattr(columns[sort_field], sort_order)()

        if not select_columns:
            query = select(self._model).offset(skip).limit(limit).order_by(order_by)
            response = await self.db.execute(query)

            return response.scalars().all()

        if select_columns:
            list_columns = []
            for col in select_columns:
                column = getattr(self._model, col)
                list_columns.append(column)
            query = select(list_columns)
            async with self.db:
                response = await self.db.execute(query)
            return response.all()

        else:
            async with self.db:
                query = select(self._model).offset(skip).limit(limit).order_by(order_by)
                response = await self.db.execute(query)
            return response.scalars().all()

    async def get_or_create(self, obj_in: CreateSchemaType, **kwargs: Any) -> ModelType:
        logger.info(
            f"\n**********GET object by [{kwargs}] or CREATE object by [{obj_in}] in table [{self._model.__table__.name.capitalize()}]"
        )  # type: ignore
        async with self.db:
            get_instance: Optional[ModelType] = await self.get(**kwargs)

            if get_instance:
                return get_instance

            instance: ModelType = await self.create(obj_in)
        return instance
