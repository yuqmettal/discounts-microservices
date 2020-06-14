from .base import CRUDBase
from database.models import Country
from database.schema import CountryCreate, CountryUpdate


class CountryCRUD(CRUDBase[Country, CountryCreate, CountryUpdate]):
    pass


country = CountryCRUD(Country)