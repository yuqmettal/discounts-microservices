from fastapi import APIRouter

from api.v1.endpoints import country
from api.v1.endpoints import province
from api.v1.endpoints import city
from api.v1.endpoints import sector
from api.v1.endpoints import address


api_router = APIRouter()

api_router.include_router(country.router, prefix='/country', tags=['countries'])
api_router.include_router(province.router, prefix='/province', tags=['provinces'])
api_router.include_router(city.router, prefix='/city', tags=['cities'])
api_router.include_router(sector.router, prefix='/sector', tags=['sectors'])
api_router.include_router(address.router, prefix='/address', tags=['addresses'])
