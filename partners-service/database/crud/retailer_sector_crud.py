from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import RetailerSector
from database.schema.retailer_sector_schema import RetailerSectorCreate, RetailerSectorUpdate


class RetailerSectorCRUD(CRUDBase[RetailerSector, RetailerSectorCreate, RetailerSectorUpdate]):
    pass


retailer_sector = RetailerSectorCRUD(RetailerSector)
