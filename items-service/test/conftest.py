from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from database import models, SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
