from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .setup import Base


class Category(Base):
    __tablename__ = "category"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('category_id_seq'),
                primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    subcategories = relationship("Subcategory", back_populates="category")
    retailers = relationship("Retailer", back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategory"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('subcategory_id_seq'),
                primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category", back_populates="subcategories")


class Retailer(Base):
    __tablename__ = "retailer"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('retailer_id_seq'),
                primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    city_id = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category", back_populates="retailers",)
    category_enabled = Column(Boolean, nullable=False, default=True)
