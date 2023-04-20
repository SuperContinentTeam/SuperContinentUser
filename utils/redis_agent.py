import os
import redis

RedisSession = redis.Redis(
    connection_pool=redis.ConnectionPool(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=os.getenv("REDIS_PORT", 6379),
        db=os.getenv("REDIS_DB", 0),
        decode_responses=True
    ),
    max_connections=100,
    decode_responses=True
)
