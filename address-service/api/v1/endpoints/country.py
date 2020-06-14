from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.crud import country
from api import get_db


router = APIRouter()


@router.get("")
async def get_all_countries(db: Session = Depends(get_db)):
    users = country.filter(db)
    return users