import asyncio

import aioredis
#adding redis
redis = aioredis.from_url(
    "redis://localhost",
    decode_responses=True,
    db=1,  # this can be useful, I can separate data into different databases like buckets.
)


async def test_get(key):
    val = await redis.get(key)
    print("key:", key, "\n", "val:", val, "\n", "value Type:", type(val), "\n")


async def test_set_and_then_get(key, value):
    await redis.set(key, value, ex=1)
    await redis.set(key, value)
    await test_get(key)
    await asyncio.sleep(1)

    await test_get(key)
    # print(await redis.scan()) #shows all keys in redis database, never should be used in prod, will kill the app, process is very heavy


# asyncio.run(test_get("test"))
asyncio.run(test_set_and_then_get("test", 3))
