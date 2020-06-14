from fastapi import APIRouter

from api.v1.endpoints import country


api_router = APIRouter()

api_router.include_router(country.router, prefix='/country', tags=['countries'])
