from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Date, Float
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
