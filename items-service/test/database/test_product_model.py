from sqlalchemy.orm import Session

from app.database import crud
from app.database.schema.product_schema import ProductCreate, ProductUpdate
from test.util.product_util import insert_product, delete_product


FILTER_PRODUCT_METHOD = 'sqlalchemy.orm.query.Query.all'
FIND_PRODUCT_METHOD = 'sqlalchemy.orm.query.Query.first'


class MockProduct:
    def __init__(self):
        self.name = 'product'

mocked_product = MockProduct()

def test_list_all_products(db: Session) -> None:
    product_count = crud.product.count(db)
    products = crud.product.filter(db)
    assert len(products) == product_count
    created = insert_product(db)
    products = crud.product.filter(db)
    assert len(products) == product_count + 1
    delete_product(db, created)


def test_get_product_by_name(db: Session, mocker) -> None:
    filter_method = mocker.patch(FIND_PRODUCT_METHOD, return_value=mocked_product)
    product = crud.product.get_by_name(db, name='product')
    assert filter_method.call_count == 1
    assert product.name == 'product'


def test_filter_products_by_name(db: Session, mocker) -> None:
    filter_method = mocker.patch(FILTER_PRODUCT_METHOD, return_value=[1,2,3,4])
    products = crud.product.filter_by_name(db, name='product')
    assert filter_method.call_count == 1


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
