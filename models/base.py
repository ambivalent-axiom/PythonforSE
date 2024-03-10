from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import Config

Base = declarative_base()
config = Config()  # type: ignore
engine = create_engine(config.postgres_host, echo=True)


def recreate_tables(engine: Engine):
    Base.metadata.drop_all(engine)  # drop all tables associated with base object
    Base.metadata.create_all(engine)  # recreate all the tables associated
