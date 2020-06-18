from sqlalchemy.orm import Session

from app.database import crud
from app.database.schema.discount_schema import DiscountCreate, DiscountUpdate
from test.util.discount_util import insert_discount, delete_discount


def test_list_all_discounts(db: Session) -> None:
    discount_count = crud.discount.count(db)
    discounts = crud.discount.filter(db)
    assert len(discounts) == discount_count
    created = insert_discount(db)
    discounts = crud.discount.filter(db)
    assert len(discounts) == discount_count + 1
    delete_discount(db, created)


def test_create_discount(db: Session) -> None:
    created = insert_discount(db)
    discount_created = crud.discount.get_by_id(db, created.id)
    assert created.id == discount_created.id
    assert created.discount == discount_created.discount
    delete_discount(db, created)


def test_update_discount(db: Session) -> None:
    created = insert_discount(db)
    discount_from_db = crud.discount.get_by_id(db, created.id)
    discount_update = DiscountUpdate(retailer_id=8)
    updated_discount = crud.discount.update(
        db, db_object=discount_from_db, object_to_update=discount_update)
    discount_from_db = crud.discount.get_by_id(db, created.id)
    assert discount_from_db.id == updated_discount.id
    assert discount_from_db.retailer_id == 8
    delete_discount(db, created)


def test_delete_discount(db: Session) -> None:
    created = insert_discount(db)

    discount_from_db = crud.discount.get_by_id(db, created.id)
    assert discount_from_db
    deleted = crud.discount.remove(db, id=created.id)
    discount_from_db = crud.discount.get_by_id(db, created.id)
    assert discount_from_db is None
    assert deleted.id == created.id
