from fastapi import APIRouter

from api.v1.endpoints import brand
from api.v1.endpoints import product


api_router = APIRouter()

api_router.include_router(brand.router, prefix='/brand', tags=['brands'])
api_router.include_router(product.router, prefix='/product', tags=['products'])
