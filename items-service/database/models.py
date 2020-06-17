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


class Discount(Base):
    id = Column(Integer, Sequence('discount_id_seq'), primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    calendarized = Column(Boolean, nullable=False, default=False)
    priority = Column(Integer, nullable=False)
    discount = Column(Float(asdecimal=True), nullable=False)
    retailer_id = Column(Integer)
    category_id = Column(Integer)
    brand_id = Column(Integer)
    subcategory_id = Column(Integer)
    by_products = Column(Boolean, nullable=False, default=False)
    by_clients = Column(Boolean, nullable=False, default=False)
    to_prime_clients = Column(Boolean, nullable=False, default=False)
    free_shipping = Column(Boolean, nullable=False, default=False)
    free_shipping_amount = Column(Float(asdecimal=True), default=0)
    according_deliver_day = Column(Boolean, nullable=False, default=False)
    according_order_day = Column(Boolean, nullable=False, default=False)
    order_and_deliver_same_day = Column(Boolean, nullable=False, default=False)
