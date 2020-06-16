from fastapi import APIRouter

from api.v1.endpoints import order
from api.v1.endpoints import order_item
from api.v1.endpoints import cart


api_router = APIRouter()

api_router.include_router(order.router, prefix='/order', tags=['orders'])
api_router.include_router(order_item.router, prefix='/order_item', tags=['order_items'])
api_router.include_router(cart.router, prefix='/cart', tags=['carts'])
