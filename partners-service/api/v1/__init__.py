from fastapi import APIRouter

from api.v1.endponts import category


api_router = APIRouter()

api_router.include_router(category.router, prefix='/category', tags=['categories'])