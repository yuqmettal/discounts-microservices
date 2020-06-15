from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from .base import CRUDBase
from database.models import City
from database.schema.city_schema import CityCreate, CityUpdate


class CityCRUD(CRUDBase[City, CityCreate, CityUpdate]):
    def get_by_province_and_name(self, db: Session, *, name: str, province_id: int):
        return db.query(self.model).filter(and_(
            self.model.name == name,
            self.model.province_id == province_id,
        )).first()


city = CityCRUD(City)
