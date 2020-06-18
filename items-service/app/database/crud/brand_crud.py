from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import Brand
from app.database.schema.brand_schema import BrandCreate, BrandUpdate


class BrandCRUD(CRUDBase[Brand, BrandCreate, BrandUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(Brand).filter(Brand.name == name).first()


brand = BrandCRUD(Brand)
