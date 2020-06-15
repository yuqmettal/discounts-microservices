from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.address_schema import Address, AddressCreate, AddressUpdate


router = APIRouter()


@router.get("/")
async def get_all_addresses(db: Session = Depends(get_db)) -> List[Address]:
    return crud.address.filter(db)


@router.post("/")
async def post_address(
    *,
    db: Session = Depends(get_db),
    address: AddressCreate
) -> Any:
    return crud.address.create(db, object_to_create=address)


@router.get("/{address_id}", response_model=Address)
async def get_address_by_id(
    *,
    db: Session = Depends(get_db),
    address_id: int,
) -> Any:
    address = crud.address.get_by_id(db, id=address_id)
    if not address:
        raise HTTPException(
            status_code=404, detail="The address doesn't exists"
        )
    return address


@router.put("/{address_id}", response_model=Address)
def update_address(
    *,
    db: Session = Depends(get_db),
    address_id: int,
    address_update: AddressUpdate,
) -> Any:
    address = crud.address.get_by_id(db, id=address_id)
    if not address:
        raise HTTPException(
            status_code=404,
            detail="The address doesn't exists",
        )
    address = crud.address.update(db, db_object=address,
                           object_to_update=address_update)
    return address


@router.delete("/{address_id}", response_model=Address)
def delete_address(
    *,
    db: Session = Depends(get_db),
    address_id: int,
) -> Any:
    address = crud.address.get_by_id(db=db, id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address = crud.address.remove(db=db, id=address_id)
    return address
