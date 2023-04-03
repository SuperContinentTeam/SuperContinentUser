from utils.redis_agent import RedisSession
from utils.reference import random_string, try_to_do
from utils.sms import SmsSender


def send_and_stash_code(email: str):
    code = random_string()
    SmsSender.send("Verification Email", code, email)
    RedisSession.client.setex(f"Code:{email}", 300, code)
    return code


@try_to_do
def check_code(email: str, code: str):
    temp = RedisSession.client.get(f"Code:{email}")
    return code == temp


def response_result(code, result):
    return {"code": code, "result": result}
