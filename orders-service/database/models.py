from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Date, Float, Text
from sqlalchemy.orm import relationship

from .setup import Base


class Order(Base):
    id = Column(Integer, Sequence('order_id_seq'),
                primary_key=True, index=True)
    retailer_id = Column(Integer, index=True, nullable=False)
    client_id = Column(Integer, index=True, nullable=False)
    address_id = Column(Integer, index=True, nullable=False)
    total_cost = Column(Float(asdecimal=True), nullable=False)
    delivery_date = Column(Date, nullable=False)
    shipping_cost = Column(Float(asdecimal=True), nullable=False)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, Sequence('order_item_id_seq'),
                primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship("Order", back_populates="items") 
    item_id = Column(Integer, index=True, nullable=False)
    pvp = Column(Float(asdecimal=True), nullable=False)
    quantity = Column(Float(asdecimal=True), nullable=False)
    notes = Column(Text)
    pvp_with_discount = Column(Float(asdecimal=True), nullable=False)
