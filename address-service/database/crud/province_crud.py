from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from .base import CRUDBase
from database.models import Province
from database.schema import ProvinceCreate, ProvinceUpdate


class ProvinceCRUD(CRUDBase[Province, ProvinceCreate, ProvinceUpdate]):
    def get_by_country_and_name(self, db: Session, *, name: str, country_id: int):
        return db.query(self.model).filter(and_(
            self.model.name == name,
            self.model.country_id == country_id,
        )).first()


province = ProvinceCRUD(Province)
