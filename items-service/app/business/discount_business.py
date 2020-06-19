from typing import List

from sqlalchemy.orm import Session

from ..database.schema.discount_schema import DiscountPOST, DiscountCreate
from ..database import crud
from ..client.partner_client import get_retailers_by_category_id, get_retailers_by_subcategory_id


def process_discount(db: Session, discount_post: DiscountPOST):
    discount = crud.discount.create(db, discount_post.discount)
    _process_discount_by_retailer_category(
        discount_id=discount.id,
        categories=discount_post.categories or [],
        retailer_id=discount.retailer_id
    )
    _process_discount_by_retailer_subcategory(
        discount_id=discount.id,
        subcategories=discount_post.subcategories or [],
        retailer_id=discount.retailer_id
    )
    _process_discount_by_brand(
        discount_id=discount.id,
        brands=discount_post.brands or []
    )
    _process_discount_by_product(
        discount_id=discount.id,
        retailer_id=discount.retailer_id,
        products=discount_post.products or []
    )
    return discount


def _process_discount_by_retailer_category(
    discount_id: int,
    categories: List,
    retailer_id: int = None
):
    categories = [x for x in categories if x]
    retailers = []
    if categories and not retailer_id:
        retailers = [x[0] for x in get_retailers_by_category_id(categories)]

    if retailer_id:
        retailers = [retailer_id]

    if not retailers:
        return

    rows_inserted = crud.discount_item.populate_from_retailer_ids(discount_id, retailers)
    return rows_inserted


def _process_discount_by_retailer_subcategory(
    discount_id: int,
    subcategories: List,
    retailer_id: int = None
):
    subcategories = [x for x in subcategories if x]
    retailers = []
    if subcategories and not retailer_id:
        retailers = [x[0]
                     for x in get_retailers_by_subcategory_id(subcategories)]

    if retailer_id:
        retailers = [retailer_id]

    if not retailers:
        return

    return crud.discount_item.populate_from_retailer_ids(discount_id, retailers)


def _process_discount_by_product(
    discount_id: int,
    retailer_id: int,
    products: List[int]
):
    products = [x for x in products if x]
    if not products:
        return
    return crud.discount_item.populate_from_product_ids(discount_id, retailer_id or 0, products)


def _process_discount_by_brand(
    discount_id: int,
    brands: List[int]
):
    brands = [x for x in brands if x]
    if not brands:
        return
    return crud.discount_item.populate_from_brand_ids(discount_id, brands)
