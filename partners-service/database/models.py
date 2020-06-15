from sqlalchemy import Column, Integer, String, Sequence

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
