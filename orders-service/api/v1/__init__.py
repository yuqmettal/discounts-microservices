from fastapi import APIRouter

from api.v1.endpoints import order


api_router = APIRouter()

api_router.include_router(order.router, prefix='/order', tags=['orders'])
