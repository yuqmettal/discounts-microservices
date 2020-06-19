from sqlalchemy.orm import Session

from app.database import crud
from app.database.schema.discount_item_schema import DiscountItemCreate, DiscountItemUpdate
from test.util.discount_item_util import insert_discount_item, delete_discount_item


def test_list_all_discount_items(db: Session) -> None:
    discount_item_count = crud.discount_item.count(db)
    discount_items = crud.discount_item.filter(db)
    assert len(discount_items) == discount_item_count
    created = insert_discount_item(db)
    discount_items = crud.discount_item.filter(db)
    assert len(discount_items) == discount_item_count + 1
    delete_discount_item(db, created)


def test_update_discount(db: Session) -> None:
    created = insert_discount_item(db)
    discount_from_db = crud.discount_item.get_by_id(db, created.id)
    discount_update = DiscountItemUpdate(discount_id=2)
    updated_discount = crud.discount_item.update(
        db, db_object=discount_from_db, object_to_update=discount_update)
    discount_from_db = crud.discount_item.get_by_id(db, created.id)
    assert discount_from_db.id == updated_discount.id
    assert discount_from_db.discount_id == 2
    delete_discount_item(db, created)

def test_create_discount_item(db: Session) -> None:
    created = insert_discount_item(db)
    discount_item_created = crud.discount_item.get_by_id(db, created.id)
    assert created.id == discount_item_created.id
    assert created.discount_id == discount_item_created.discount_id
    delete_discount_item(db, created)


def test_delete_discount_item(db: Session) -> None:
    created = insert_discount_item(db)

    discount_item_from_db = crud.discount_item.get_by_id(db, created.id)
    assert discount_item_from_db
    deleted = crud.discount_item.remove(db, id=created.id)
    discount_item_from_db = crud.discount_item.get_by_id(db, created.id)
    assert discount_item_from_db is None
    assert deleted.id == created.id
