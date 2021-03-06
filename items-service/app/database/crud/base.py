from pydantic import BaseModel

from typing import Generic, Type, TypeVar, Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def paging(self, db: Session, *, page: int = 1, size: int = 100) -> List[ModelType]:
        skip = (page - 1) * size
        return self.filter(db=db, skip=skip, limit=size)

    def filter(self, db: Session, *, skip: int = None, limit: int = None) -> List[ModelType]:
        main_query = db.query(self.model)
        if None not in [skip, limit]:
            main_query = main_query.offset(skip).limit(limit)
        return main_query.all()

    def create(self, db: Session, object_to_create: CreateSchemaType) -> ModelType:
        object_data = jsonable_encoder(object_to_create)
        db_object = self.model(**object_data)
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def update(self, db: Session, *, db_object: ModelType, object_to_update: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        object_data = jsonable_encoder(db_object)
        if isinstance(object_to_update, dict):
            update_data = object_to_update
        else:
            update_data = object_to_update.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def count(self, db: Session) -> int:
        return db.query(self.model).count()
