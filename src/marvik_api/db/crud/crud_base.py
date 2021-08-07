import abc
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from marvik_api.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDAbstract(abc.ABC):
    @abc.abstractmethod
    def get(self):  # pragma: nocover
        pass

    @abc.abstractmethod
    def get_by_name(self):  # pragma: nocover
        pass

    @abc.abstractmethod
    def create(self):  # pragma: nocover
        pass

    @abc.abstractmethod
    def update(self):  # pragma: nocover
        pass

    @abc.abstractmethod
    def delete(self):  # pragma: nocover
        pass


class CRUDBase(
    CRUDAbstract, Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]
):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    **Parameters**
    * model: A SQLAlchemy model class
    * schema: A Pydantic model (schema) class
    """

    def __init__(
        self, session_db: Session, model: Type[ModelType], schema: Type[SchemaType]
    ):
        self.db = session_db
        self.model = model
        self.schema = schema

    def get(self, id_db: Any) -> Optional[ModelType]:
        db_obj = self.db.query(self.model).filter(self.model.id == id_db).first()
        return db_obj

    def get_by_name(self, *, name: str) -> Optional[ModelType]:
        db_obj = self.db.query(self.model).filter(self.model.name == name).first()
        return db_obj

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        self._commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        self._commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, *, id_db: int) -> ModelType:
        db_obj = self.db.query(self.model).get(id_db)
        self.db.delete(db_obj)
        self._commit()
        return db_obj

    def _commit(self):
        try:
            self.db.commit()
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise exc
