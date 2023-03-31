import redis

from utils.environments import Env


class _RedisSession:
    def __init__(self):
        self.client = redis.Redis(connection_pool=redis.ConnectionPool(
            host=Env.REDIS_HOST,
            port=Env.REDIS_PORT,
            decode_responses=True,
            db=1
        ))


RedisSession = _RedisSession()
