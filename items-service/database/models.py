from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import relationship

from .setup import Base


class Brand(Base):
    id = Column(Integer, Sequence('brand_id_seq'), primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    products = relationship("Product", back_populates="brand")


class Product(Base):
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tax_rate = Column(Float(asdecimal=True), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    brand = relationship("Brand", back_populates="products") 
    items = relationship("Item", back_populates="product")


class Item(Base):
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True, index=True)
    retailer_id = Column(Integer, index=True, nullable=False)
    category_id = Column(Integer, index=True, nullable=False)
    pvp = Column(Float(asdecimal=True), nullable=False)
    margin = Column(Float(asdecimal=True), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product", back_populates="items") 
