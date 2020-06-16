import os
import json

import settings
from database import crud, SessionLocal
from database.schema.order_schema import OrderCreate


def seed_data():
    seed_order_data()


def seed_order_data():
    order_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'orders.json'
    )
    with open(order_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for order_data in data:
            order = crud.order.get_by_id(db=db, id=order_data['id'])
            if not order:
                order = OrderCreate(**order_data)
                crud.order.create(db, object_to_create=order)