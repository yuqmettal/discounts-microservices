from .base import CRUDBase
from database.models import Address
from database.schema.address_schema import AddressCreate, AddressUpdate


class AddressCRUD(CRUDBase[Address, AddressCreate, AddressUpdate]):
    pass

address = AddressCRUD(Address)
