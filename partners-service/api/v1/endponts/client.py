from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import crud
from api import get_db
from database.schema.client_schema import Client, ClientCreate, ClientUpdate


router = APIRouter()


@router.get("/")
async def get_all_clientes(db: Session = Depends(get_db)) -> List[Client]:
    return crud.client.filter(db)


@router.post("/")
async def post_client(
    *,
    db: Session = Depends(get_db),
    client: ClientCreate
) -> Any:
    client_by_name = crud.client.get_by_email(db, email=client.email)
    if client_by_name:
        raise HTTPException(
            status_code=400,
            detail=f"The Client with email '{client.email}' already exists",
        )
    return crud.client.create(db, object_to_create=client)


@router.get("/{client_id}", response_model=Client)
async def get_client_by_id(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    client = crud.client.get_by_id(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=404, detail="The client doesn't exists"
        )
    return client


@router.put("/{client_id}", response_model=Client)
def update_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
    client_update: ClientUpdate,
) -> Any:
    client = crud.client.get_by_id(db, id=client_id)
    if not client:
        raise HTTPException(
            status_code=404,
            detail="The client doesn't exists",
        )
    client = crud.client.update(db, db_object=client,
                           object_to_update=client_update)
    return client


@router.delete("/{client_id}", response_model=Client)
def delete_client(
    *,
    db: Session = Depends(get_db),
    client_id: int,
) -> Any:
    client = crud.client.get_by_id(db=db, id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client = crud.client.remove(db=db, id=client_id)
    return client
