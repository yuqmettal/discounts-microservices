from fastapi import APIRouter

from api.v1.endpoints import country
from api.v1.endpoints import province


api_router = APIRouter()

api_router.include_router(country.router, prefix='/country', tags=['countries'])
api_router.include_router(province.router, prefix='/province', tags=['provinces'])
