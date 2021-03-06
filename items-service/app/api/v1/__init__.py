from fastapi import APIRouter

from app.api.v1.endpoints import brand
from app.api.v1.endpoints import product
from app.api.v1.endpoints import item
from app.api.v1.endpoints import discount


api_router = APIRouter()

api_router.include_router(brand.router, prefix='/brand', tags=['brands'])
api_router.include_router(product.router, prefix='/product', tags=['products'])
api_router.include_router(item.router, prefix='/item', tags=['items'])
api_router.include_router(discount.router, prefix='/discount', tags=['discounts'])
