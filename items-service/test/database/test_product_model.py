from sqlalchemy.orm import Session

from database import crud
from database.schema.product_schema import ProductCreate, ProductUpdate
from test.util.product_util import insert_product, delete_product


def test_list_all_products(db: Session) -> None:
    product_count = crud.product.count(db)
    products = crud.product.filter(db)
    assert len(products) == product_count
    created = insert_product(db)
    products = crud.product.filter(db)
    assert len(products) == product_count + 1
    delete_product(db, created)


def test_create_product(db: Session) -> None:
    created = insert_product(db)
    product_created = crud.product.get_by_id(db, created.id)
    assert created.id == product_created.id
    assert created.name == product_created.name
    delete_product(db, created)


def test_update_product(db: Session) -> None:
    created = insert_product(db)
    product_from_db = crud.product.get_by_id(db, created.id)
    product_update = ProductUpdate(name="Changed")
    updated_product = crud.product.update(
        db, db_object=product_from_db, object_to_update=product_update)
    product_from_db = crud.product.get_by_id(db, created.id)
    assert product_from_db.id == updated_product.id
    assert product_from_db.name == "Changed"
    delete_product(db, created)


def test_delete_product(db: Session) -> None:
    created = insert_product(db)

    product_from_db = crud.product.get_by_id(db, created.id)
    assert product_from_db
    deleted = crud.product.remove(db, id=created.id)
    product_from_db = crud.product.get_by_id(db, created.id)
    assert product_from_db is None
    assert deleted.id == created.id
