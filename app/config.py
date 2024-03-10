from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    postgres_host: str = Field("postgresql://ambax:black@localhost:5432/pythonforSE")
    redis_host: str = Field("redis://localhost")

    class Config:
        env_prefix = "db_"
