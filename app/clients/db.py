import os
from typing import Optional, Union

from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Row
from sqlalchemy.sql.expression import Delete, Insert, Select

from app.config import Config


class DatabaseClient:
    def __init__(self, config: Config, tables: Optional[list[str]]):
        self.config = config
        self.engine = create_engine(self.config.postgres_host, future=True)
        self.metadata = MetaData()  # engine was not supposed to be passed in here
        self._reflect_metadata(
            self.engine
        )  # metadata.tables['user'] - instead engine went in here
        if tables:  # does not trigger if tables is None, or len(tables) == 0
            self._set_internal_database_tables(tables)
        # if os.getenv("app_env") == "test":
        #     self.database = Database(self.config.host, force_rollback=True)
        # else:
        self.database = Database(self.config.postgres_host)

    def _reflect_metadata(self, engine) -> None:
        self.engine = engine  # here goes the engine
        self.metadata.reflect(
            bind=self.engine
        )  # and eventually binds with metadata.reflect

    async def connect(self) -> None:
        await self.database.connect()

    async def disconnect(self) -> None:
        await self.database.disconnect()

    def _set_internal_database_tables(self, tables: list[str]):
        # e.g. sets DatabaseClient.user = DatabaseClient.metadata.tables["user"] if "user" in tables
        self.user = self.metadata.tables["user"]
        self.liked_post = self.metadata.tables["liked_post"]

        # for table in tables:
        #     setattr(self, table, self.metadata.tables[table])

    async def get_first(self, query: Union[Select, Insert]) -> Optional[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_one(query)
        # here is the previous sync method
        # with self.session.begin():
        #     res = self.session.execute(query)#.first()
        return res

    async def get_all(self, query: Select) -> list[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_all(query)
        # with self.session.begin():
        #     res = self.session.execute(query)#.all()
        return res

    async def get_paginated(self, query: Select, limit: int, offset: int) -> list[Row]:
        query = query.limit(limit).offset(offset)
        return await self.get_all(query)

    async def execute_in_transaction(self, query: Delete):
        async with self.database.transaction():
            await self.database.execute(query)
        # with self.session.begin():
        #     self.session.execute(query)
