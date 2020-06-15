from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from .base import CRUDBase
from database.models import Sector
from database.schema.sector_schema import SectorCreate, SectorUpdate


class SectorCRUD(CRUDBase[Sector, SectorCreate, SectorUpdate]):
    def get_by_city_and_name(self, db: Session, *, name: str, city_id: int):
        return db.query(self.model).filter(and_(
            self.model.name == name,
            self.model.city_id == city_id,
        )).first()


sector = SectorCRUD(Sector)
