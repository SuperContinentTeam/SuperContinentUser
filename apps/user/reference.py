from aioredis import Redis

from utils.reference import try_to_do


@try_to_do
def check_code(email: str, code: str, redis: Redis):
    temp = redis.get(f"Code:{email}")
    return code == temp


def response_result(code, result):
    return {"code": code, "result": result}
