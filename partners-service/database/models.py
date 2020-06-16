from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Date
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
    category = relationship("Category", back_populates="retailers")
    category_enabled = Column(Boolean, nullable=False, default=True)
    retailer_sectors = relationship("RetailerSector", back_populates="retailer")


class RetailerSector(Base):
    __tablename__ = "retailer_sector"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('retailer_sector_id_seq'),
                primary_key=True, index=True)
    enabled = Column(Boolean, nullable=False, default=True)
    sector_id = Column(Integer, nullable=False)
    
    retailer_id = Column(Integer, ForeignKey('retailer.id'), nullable=False)
    retailer = relationship("Retailer", back_populates="retailer_sectors")


class Client(Base):
    __tablename__ = "client"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('client_id_seq'),
                primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    client_prime_subscriptions = relationship("ClientPrimeSubscription", back_populates="client")


class PrimeSubscription(Base):
    __tablename__ = "prime_subscription"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('prime_subscription_id_seq'),
                primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    validity = Column(Integer)
    validity_type = Column(String)
    enabled = Column(Boolean, nullable=False, default=True)
    client_prime_subscriptions = relationship("ClientPrimeSubscription", back_populates="prime_subscription")


class ClientPrimeSubscription(Base):
    __tablename__ = "client_prime_subscription"

    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, Sequence('prime_subscription_id_seq'),
                primary_key=True, index=True)
    activation_date = Column(Date)
    subscription_state = Column(String)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    client = relationship("Client", back_populates="client_prime_subscriptions")
    prime_subscription_id = Column(Integer, ForeignKey('prime_subscription.id'), nullable=False)
    prime_subscription = relationship("PrimeSubscription", back_populates="client_prime_subscriptions")
