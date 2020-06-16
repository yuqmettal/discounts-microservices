import os
import json

import settings
from database import crud, SessionLocal
from database.schema.order_schema import OrderCreate
from database.schema.order_item_schema import OrderItemCreate
from database.schema.cart_schema import CartCreate
from database.schema.cart_item_schema import CartItemCreate


def seed_data():
    seed_order_data()
    seed_order_item_data()
    seed_cart_item_data()


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


def seed_order_item_data():
    order_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'order_items.json'
    )
    with open(order_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for order_item_data in data:
            order_item = crud.order_item.get_by_id(db=db, id=order_item_data['id'])
            if not order_item:
                order_item = OrderItemCreate(**order_item_data)
                crud.order_item.create(db, object_to_create=order_item)


def seed_cart_data():
    order_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'carts.json'
    )
    with open(order_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for cart_data in data:
            cart = crud.cart.get_by_id(db=db, id=cart_data['id'])
            if not cart:
                cart = CartCreate(**cart_data)
                crud.cart.create(db, object_to_create=cart)


def seed_cart_item_data():
    order_file = os.path.join(
        settings.BASE_DIR,
        'database',
        'data',
        'cart_items.json'
    )
    with open(order_file) as json_file:
        data = json.load(json_file)
        db = SessionLocal()
        for cart_items_data in data:
            cart_item = crud.cart_item.get_by_id(db=db, id=cart_items_data['id'])
            if not cart_item:
                cart_item = CartItemCreate(**cart_items_data)
                crud.cart_item.create(db, object_to_create=cart_item)
