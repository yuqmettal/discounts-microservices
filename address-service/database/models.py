from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .setup import Base


class Country(Base):
    __tablename__ = "country"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, primary_key=True, index=True)
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

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country", back_populates="provinces")
    name = Column(String, index=True, nullable=False)
    region = Column(String, nullable=False)
