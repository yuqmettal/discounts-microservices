from .base import EurekaClient, EurekaResponse
from .schemas.address_schema import Address


_address_client = EurekaClient('address-service')


def get_address_by_id(id: int) -> Address:
    endpoint = f'/api/v1/address/{id}'
    response: EurekaResponse = _address_client.remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Address(**response.content)