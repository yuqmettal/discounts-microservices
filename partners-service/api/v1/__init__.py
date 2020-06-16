from fastapi import APIRouter

from api.v1.endponts import category
from api.v1.endponts import subcategory
from api.v1.endponts import retailer
from api.v1.endponts import retailer_sector


api_router = APIRouter()

api_router.include_router(category.router, prefix='/category', tags=['categories'])
api_router.include_router(subcategory.router, prefix='/subcategory', tags=['subcategories'])
api_router.include_router(retailer.router, prefix='/retailer', tags=['retailers'])
api_router.include_router(retailer_sector.router, prefix='/retailer_sector', tags=['retailer_sectors'])
