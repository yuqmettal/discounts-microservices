from fastapi import APIRouter

from api.v1.endponts import category
from api.v1.endponts import subcategory


api_router = APIRouter()

api_router.include_router(category.router, prefix='/category', tags=['categories'])
api_router.include_router(subcategory.router, prefix='/subcategory', tags=['subcategories'])