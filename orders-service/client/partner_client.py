from .base import EurekaClient, EurekaResponse
from .schemas.client_schema import Client
from .schemas.retailer_schema import Retailer


_partner_retailer_client = EurekaClient('partners-service')
_partner_client_client = EurekaClient('partners-service')


def get_retailer_by_id(id: int) -> Retailer:
    endpoint = f'/api/v1/retailer/{id}'
    response: EurekaResponse = _partner_retailer_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Retailer(**response.content)


def get_client_by_id(id: int) -> Client:
    endpoint = f'/api/v1/client/{id}'
    response: EurekaResponse = _partner_client_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Client(**response.content)
