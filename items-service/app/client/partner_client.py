from .base import EurekaClient, EurekaResponse
from .schemas.category_schema import Category
from .schemas.retailer_schema import Retailer


_partner_retailer_client = EurekaClient('partners-service')
_partner_category_client = EurekaClient('partners-service')


def get_retailer_by_id(id: int) -> Retailer:
    endpoint = f'/api/v1/retailer/{id}'
    response: EurekaResponse = _partner_retailer_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Retailer(**response.content)


def get_category_by_id(id: int) -> Category:
    endpoint = f'/api/v1/category/{id}'
    response: EurekaResponse = _partner_category_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Category(**response.content)
