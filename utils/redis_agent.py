import aioredis

from utils.environments import Env

_CACHE = dict()
_CLIENT = "redis_client"


async def get_redis_pool():
    if _CLIENT not in _CACHE:
        _CACHE[_CLIENT] = await aioredis.from_url(Env.REDIS_URL, encoding="utf-8", decode_responses=True)

    return _CACHE[_CLIENT]
