from sqlalchemy.orm import Session

from app.database import crud
from app.database.schema.brand_schema import BrandCreate, BrandUpdate
from test.util.brand_util import insert_brand, delete_brand


def test_list_all_brands(db: Session) -> None:
    brand_count = crud.brand.count(db)
    brands = crud.brand.filter(db)
    assert len(brands) == brand_count
    created = insert_brand(db)
    brands = crud.brand.filter(db)
    assert len(brands) == brand_count + 1
    delete_brand(db, created)


def test_create_brand(db: Session) -> None:
    created = insert_brand(db)
    brand_created = crud.brand.get_by_id(db, created.id)
    assert created.id == brand_created.id
    assert created.name == brand_created.name
    delete_brand(db, created)


def test_update_brand(db: Session) -> None:
    created = insert_brand(db)
    brand_from_db = crud.brand.get_by_id(db, created.id)
    brand_update = BrandUpdate(name="Changed")
    updated_brand = crud.brand.update(
        db, db_object=brand_from_db, object_to_update=brand_update)
    brand_from_db = crud.brand.get_by_id(db, created.id)
    assert brand_from_db.id == updated_brand.id
    assert brand_from_db.name == "Changed"
    delete_brand(db, created)


def test_delete_brand(db: Session) -> None:
    created = insert_brand(db)

    brand_from_db = crud.brand.get_by_id(db, created.id)
    assert brand_from_db
    deleted = crud.brand.remove(db, id=created.id)
    brand_from_db = crud.brand.get_by_id(db, created.id)
    assert brand_from_db is None
    assert deleted.id == created.id
