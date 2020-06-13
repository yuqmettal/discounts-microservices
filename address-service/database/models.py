from sqlalchemy import Column, Integer, String

from .setup import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False)
    currency = Column(String, nullable=False)
