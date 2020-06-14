from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Country
from database.schema import CountryCreate, CountryUpdate


class CountryCRUD(CRUDBase[Country, CountryCreate, CountryUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Country).filter(Country.name == name).first()

    def get_by_code(self, db: Session, *, code: str):
        return db.query(Country).filter(Country.code == code).first()


country = CountryCRUD(Country)
