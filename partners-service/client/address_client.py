from .base import EurekaClient, EurekaResponse
from .schemas.city_schema import City
from .schemas.sector_schema import Sector


_address_client = EurekaClient('address-service')


def get_city_by_id(id: int) -> City:
    endpoint = f'/api/v1/city/{id}'
    response: EurekaResponse = _address_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return City(**response.content)


def get_sector_by_id(id: int) -> Sector:
    endpoint = f'/api/v1/sector/{id}'
    response: EurekaResponse = _address_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Sector(**response.content)
