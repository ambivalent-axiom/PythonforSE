import logging
import pickle

import aioredis

from app.config import Config

logger = logging.getLogger(__name__)


class RedisCache:
    user_prefix = "user"
    pagination_prefix = "pagination"

    def __init__(self, config: Config, ttl: int = 300):
        self._host = config.redis_host
        self.redis = aioredis.from_url(self._host, db=0)
        self.ttl = ttl

    async def get(self, key, prefix):
        try:
            storage_key = f"{prefix}:{key}"  # in case of - user:1, in case of - post:1
            val = await self.redis.get(storage_key)
            return pickle.loads(val)
        except Exception as e:
            logger.error(
                f"Encounterd err {str(e)} when tried to read prefix: {prefix} and key: {key}"
            )
        return

    async def set(self, key, value, prefix):
        try:
            storage_key = f"{prefix}:{key}"
            serialized_value = pickle.dumps(value)
            await self.redis.set(storage_key, serialized_value, ex=self.ttl)
        except Exception as e:
            logger.error(
                f"Encounterd err {str(e)} when tried to save {value} to {storage_key}"
            )
        return

    async def delete(self, *args, prefix):
        try:
            prefixed_args = [f"{prefix}:{key}" for key in args]
            await self.redis.delete(
                *prefixed_args
            )  # redis.delte("user:1", "user:2"....)
        except Exception as e:
            logger.error(
                f"Encounterd err {str(e)} when tried to delete {prefixed_args}"
            )
        return

    # REDIS HASH AND SETS
    async def hget(self, name, key, prefix):
        try:
            storage_name = self.create_storage_name(name, prefix)
            val = await self.redis.hget(storage_name, key)
            # pickled_val = pickle.dumps(val)
            return val
        except Exception as e:
            logger.error(
                f"Encounterd err {str(e)} when tried to read prefix: {prefix} and key: {key}"
            )
        return

    async def hset(self, name, mapping, prefix):
        storage_name = self.create_storage_name(name, prefix)
        serialized_mapping = {}
        for key in mapping:
            serialized_mapping[key] = pickle.dumps(mapping[key])
        await self.redis.hset(storage_name, mapping=mapping)
        await self.redis.expire(storage_name, self.ttl)

    async def hdel(self, name, key, prefix):
        storage_name = self.create_storage_name(name, prefix)
        await self.redis.hdel(storage_name, key)

    async def sadd(self, name, key, prefix):
        storage_name = self.create_storage_name(name, prefix)
        await self.redis.sadd(storage_name, key)

    # HELPER METHODS
    def get_pagination_key(self, limit):
        return f"{self.pagination_prefix}:{limit}"

    def get_pagination_set_key(self):
        return f"{self.pagination_prefix}"

    async def clear_pagination_cache(self, prefix):
        set_storage_name = self.create_storage_name(
            self.get_pagination_set_key(), prefix
        )
        limits = await self.redis.smembers(set_storage_name)
        print("got limits:", limits)
        for limit in limits:
            pagination_storage_key = f"{prefix}:{self.get_pagination_key(limit)}"
            await self.redis.delete(pagination_storage_key)
            await self.redis.srem(set_storage_name, limit)

    async def flush_db(self) -> None:
        await self.redis.flushdb(
            asynchronous=True
        )  # flushes current db, .flushall() flushes all db's

    @staticmethod
    def create_storage_name(key, prefix):
        return f"{prefix}:{key}"
