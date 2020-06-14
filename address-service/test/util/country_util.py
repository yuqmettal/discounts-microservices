from database.schema import CountryCreate
from .utils import random_lower_string, random_upper_string


def create_random_country():
    name = random_lower_string()
    code = random_upper_string()
    language = random_upper_string()
    currency = random_upper_string()
    return CountryCreate(name=name, code=code, language=language, currency=currency)


def create_random_country_data():
    name = random_lower_string()
    code = random_upper_string()
    language = random_upper_string()
    currency = random_upper_string()
    return {'name': name, 'code': code, 'language': language, 'currency': currency}
