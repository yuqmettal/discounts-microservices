from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship

from .setup import Base


class Brand(Base):
    id = Column(Integer, Sequence('brand_id_seq'), primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
