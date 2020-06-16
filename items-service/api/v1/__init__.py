from fastapi import APIRouter

from api.v1.endpoints import brand
from api.v1.endpoints import product
from api.v1.endpoints import item


api_router = APIRouter()

api_router.include_router(brand.router, prefix='/brand', tags=['brands'])
api_router.include_router(product.router, prefix='/product', tags=['products'])
api_router.include_router(item.router, prefix='/item', tags=['items'])
