from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


from database import models



SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
    models.Base.metadata.drop_all(bind=engine)
