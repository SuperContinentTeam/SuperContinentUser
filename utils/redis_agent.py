import aioredis

from utils.environments import Env

REDIS_POOL = None


async def get_redis_pool():
    global REDIS_POOL
    if REDIS_POOL is None:
        REDIS_POOL = await aioredis.from_url(Env.REDIS_URL, encoding="utf-8", decode_responses=True)

    return REDIS_POOL
