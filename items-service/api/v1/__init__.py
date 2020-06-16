from fastapi import APIRouter

from api.v1.endpoints import brand


api_router = APIRouter()

api_router.include_router(brand.router, prefix='/brand', tags=['brands'])
