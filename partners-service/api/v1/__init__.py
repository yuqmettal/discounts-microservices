from fastapi import APIRouter

from api.v1.endponts import category
from api.v1.endponts import subcategory
from api.v1.endponts import retailer
from api.v1.endponts import retailer_sector
from api.v1.endponts import client
from api.v1.endponts import prime_subscription
from api.v1.endponts import client_prime_subscription


api_router = APIRouter()

api_router.include_router(category.router, prefix='/category', tags=['categories'])
api_router.include_router(subcategory.router, prefix='/subcategory', tags=['subcategories'])
api_router.include_router(retailer.router, prefix='/retailer', tags=['retailers'])
api_router.include_router(retailer_sector.router, prefix='/retailer_sector', tags=['retailer_sectors'])
api_router.include_router(client.router, prefix='/client', tags=['clients'])
api_router.include_router(prime_subscription.router, prefix='/prime_subscription', tags=['prime_subscriptions'])
api_router.include_router(client_prime_subscription.router, prefix='/client_prime_subscription', tags=['client_prime_subscription'])
