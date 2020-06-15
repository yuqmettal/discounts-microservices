from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Retailer
from database.schema.retailer_schema import RetailerCreate, RetailerUpdate


class RetailerCRUD(CRUDBase[Retailer, RetailerCreate, RetailerUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Retailer).filter(Retailer.name == name).first()


retailer = RetailerCRUD(Retailer)
