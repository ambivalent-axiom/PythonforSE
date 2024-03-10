from fastapi import FastAPI

from app import create_user_router
from app.clients.db import DatabaseClient
from app.clients.redis import RedisCache
from app.config import Config
from app.exception_handlers import add_exception_handlers


def create_application() -> FastAPI:
    config = Config()  # type: ignore
    tables = ["user", "liked_post"]
    redis_cache = RedisCache(config)
    database_client = DatabaseClient(config, tables)
    user_router = create_user_router(database_client, redis_cache)
    app = FastAPI()
    app.include_router(user_router)
    add_exception_handlers(app)
    return app
