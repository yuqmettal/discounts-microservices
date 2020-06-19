from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import Item
from app.database.schema.item_schema import ItemCreate, ItemUpdate
from ...database import engine


class ItemCRUD(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_items_with_descount(self, page: int = 1, size: int = 0):
        skip = (page - 1) * size
        query = f"""select c.*, a.name, a.description, a.tax_rate, a.brand_id, coalesce((
                   select x.discount from discount x 
                       join discount_item y on x.id = y.discount_id 
                   where y.item_id = c.id 
                   order by x.priority desc 
                   fetch first 1 rows only), 0) as discount 
               from item c join product a on a.id = c.product_id 
               limit {size} offset {skip}"""

        with engine.connect() as con:
            rs = con.execute(query).fetchall()
            results = []
            for row_number, row in enumerate(rs):
                results.append({})
                for column_number, value in enumerate(row):
                    results[row_number][row.keys()[column_number]] = value
            return results


item = ItemCRUD(Item)
