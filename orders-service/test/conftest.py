from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from database import models, SessionLocal, engine
from database.data.seed_data import seed_data


models.Base.metadata.create_all(bind=engine)
seed_data()


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
