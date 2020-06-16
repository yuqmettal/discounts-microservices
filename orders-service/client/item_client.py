from .base import EurekaClient, EurekaResponse
from .schemas.item_schema import Item


_item_client = EurekaClient('items-service')


def get_item_by_id(id: int) -> Item:
    endpoint = f'/api/v1/item/{id}'
    response: EurekaResponse = _item_client.call_remote_service(endpoint, "GET")
    if response.status != 200:
        return None
    return Item(**response.content)
