from typing import List

from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import DiscountItem
from app.database.schema.discount_item_schema import DiscountItemCreate, DiscountItemUpdate
from ...database import engine


class DiscountItemCRUD(CRUDBase[DiscountItem, DiscountItemCreate, DiscountItemUpdate]):
    def get_by_discount(self, db: Session, *, discount_id: int):
        return db.query(DiscountItem).filter(DiscountItem.discount_id == discount_id).all()

    def populate_from_retailer_ids(self, discount_id: int, retailers: List[int]):
        ids = ','.join(str(x) for x in retailers)
        with engine.connect() as con:
            query = f"""
                insert into discount_item(id, discount_id, item_id)
                select nextval('discount_item_id_seq'),{discount_id} as discount_id,
                 id as item_id from item where retailer_id in ({ids})
                 and id not in (select item_id from discount_item where discount_id = {discount_id})
            """
            rs = con.execute(query)
            return rs.rowcount

    def populate_from_product_ids(self, discount_id: int, retailer_id: int, products: List[int]):
        ids = ','.join(str(x) for x in products)
        with engine.connect() as con:
            query = f"""
            insert into discount_item(id, discount_id, item_id)
            select 
                    nextval('discount_item_id_seq'),
                    {discount_id} as discount_id,
                    id as item_id 
            from item 
            where product_id in (1)
            and retailer_id in (select distinct(retailer_id)
            from item
            where retailer_id not in ({retailer_id}))
            and id not in (select item_id from discount_item where discount_id = {discount_id})
            """
            rs = con.execute(query)
            return rs.rowcount

    def populate_from_brand_ids(self, discount_id: int, brands: List[int]):
        ids = ','.join(str(x) for x in brands)
        with engine.connect() as con:
            query = f"""
            insert into discount_item(id, discount_id, item_id)
            select 
                    nextval('discount_item_id_seq'),
                    {discount_id} as discount_id,
                    a.id as item_id 
            from item a
            join product b on a.product_id = b.id
            where b.brand_id in ({ids})
            and a.id not in (select item_id from discount_item where discount_id = {discount_id})
            """
            rs = con.execute(query)
            return rs.rowcount


discount_item = DiscountItemCRUD(DiscountItem)
