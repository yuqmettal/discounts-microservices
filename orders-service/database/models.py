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


class Cart(Base):
    id = Column(Integer, Sequence('cart_id_seq'), primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_item'

    id = Column(Integer, Sequence('cart_item_id_seq'), primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)
    cart = relationship("Cart", back_populates="cart_items")
    quantity = Column(Float(asdecimal=True), nullable=False)
    notes = Column(Text)
    item_id = Column(Integer, nullable=False)
