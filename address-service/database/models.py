from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from .setup import Base


class Country(Base):
    __tablename__ = "country"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('country_id_seq'), primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    provinces = relationship("Province", back_populates="country")


class Province(Base):
    __tablename__ = "province"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('province_id_seq'),primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country", back_populates="provinces")
    name = Column(String, index=True, nullable=False)
    region = Column(String, nullable=False)
    cities = relationship("City", back_populates="province")


class City(Base):
    __tablename__ = "city"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('city_id_seq'), primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey('province.id'))
    province = relationship("Province", back_populates="cities")
    name = Column(String, index=True, nullable=False)
    sectors = relationship("Sector", back_populates="city")


class Sector(Base):
    __tablename__ = "sector"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('sector_id_seq'), primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="sectors")
    name = Column(String, index=True, nullable=False)
    addresses = relationship("Address", back_populates="sector")


class Address(Base):
    __tablename__ = "address"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('address_id_seq'), primary_key=True, index=True)
    sector_id = Column(Integer, ForeignKey('sector.id'))
    sector = relationship("Sector", back_populates="addresses")
    name = Column(String, index=True, nullable=False)
    line_one = Column(String)
    line_two = Column(String)
