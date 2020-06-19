from app.business.discount_business import (
    process_discount,
    _process_discount_by_retailer_category,
    _process_discount_by_retailer_subcategory,
    _process_discount_by_product,
    _process_discount_by_brand
)
from app.database import crud


CREATE_DISCOUNT_METHOD = 'app.database.crud.discount.create'
PARTNER_CLIENT_METHOD = 'app.client.partner_client._partner_retailer_client.call_remote_service'
POPULATE_RETAILER_METHOD = 'app.database.crud.discount_item.populate_from_retailer_ids'
POPULATE_RETAILER_PRODUCTS_METHOD = 'app.database.crud.discount_item.populate_from_product_ids'
POPULATE_RETAILER_BRANDS_METHOD = 'app.database.crud.discount_item.populate_from_brand_ids'


class MockReponse:
    def __init__(self, status: int, content: list):
        self.status = status
        self.content = content


class MockDiscount:
    def __init__(self, id: int, discount: dict):
        self.id = id
        self.discount = discount
        self.categories = []
        self.subcategories = []
        self.brands = []
        self.products = []
        self.retailer_id = 0


mocked_discount = MockDiscount(1, {})
mocked_response = MockReponse(status=200, content=[[1], [2]])


def test_process_discount(mocker):
    mocker.patch(CREATE_DISCOUNT_METHOD, return_value=mocked_discount)
    mocker.patch(PARTNER_CLIENT_METHOD, return_value=mocked_response)
    mocker.patch(POPULATE_RETAILER_METHOD, return_value=999)
    mocker.patch(POPULATE_RETAILER_BRANDS_METHOD, return_value=999)
    mocker.patch(POPULATE_RETAILER_PRODUCTS_METHOD, return_value=999)
    discount_post = MockDiscount(2, {})
    discount = process_discount(None, discount_post)
    discount.id == mocked_discount.id


def test_process_discount_by_retailer_category(mocker):
    mocker.patch(PARTNER_CLIENT_METHOD, return_value=mocked_response)
    mocker.patch(POPULATE_RETAILER_METHOD, return_value=999)
    rows_affected = _process_discount_by_retailer_category(1, [1, 2, 3])
    assert rows_affected == 999


def test_process_discount_by_retailer_subcategory(mocker):
    mocker.patch(PARTNER_CLIENT_METHOD, return_value=mocked_response)
    mocker.patch(POPULATE_RETAILER_METHOD, return_value=999)
    rows_affected = _process_discount_by_retailer_subcategory(1, [1, 2, 3])
    assert rows_affected == 999


def test_process_discount_by_product(mocker):
    mocker.patch(POPULATE_RETAILER_PRODUCTS_METHOD, return_value=999)
    rows_affected = _process_discount_by_product(1, 0, [1, 2, 3])
    assert rows_affected == 999


def test_process_discount_by_brands(mocker):
    mocker.patch(POPULATE_RETAILER_BRANDS_METHOD, return_value=999)
    rows_affected = _process_discount_by_brand(1, [1, 2, 3])
    assert rows_affected == 999
