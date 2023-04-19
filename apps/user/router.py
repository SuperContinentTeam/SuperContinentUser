from fastapi import APIRouter, Depends
from fastapi.requests import Request

from adapter.tencent_sms import SmsAdapter
from utils.redis_agent import RedisSession
from utils.reference import random_string
from .interface import build_jwt, decode_token
from .models import User
from .reference import response_result, check_code, parse_body

router = APIRouter(prefix="/user")


@router.post("/send-code")
async def send_code(body: dict = Depends(parse_body)):
    email = body["recipient"]
    code = random_string(length=12)
    await SmsAdapter.send_code([email], "Verification", code)
    # 缓存300秒
    RedisSession.setex(f"Code:{email}", 300, code.encode())
    return code


@router.post("/register")
async def register(body: dict = Depends(parse_body)):
    if await User.filter(username=body["username"]).exists():
        return response_result(2, "This username has been registered")
    if await User.filter(email=body["email"]).exists():
        return response_result(3, "This email has been registered")

    status, result = check_code(body["email"], body["code"], RedisSession)
    if not status or not result:
        return response_result(4, "Verification code has expired")

    entity_id = random_string(8)
    while await User.filter(entity_id=entity_id).exists():
        entity_id = random_string(8)

    user = User(entity_id=entity_id, username=body["username"], email=body["email"])
    user.set_password(body["password"])
    await user.save()

    return response_result(1, user)


@router.post("/login")
async def login(body: dict = Depends(parse_body)):
    if not (user := await User.filter(username=body["username"]).first()):
        return response_result(0, "User not found")

    if not user.check_password(body["password"]):
        return response_result(0, "Invalid password")

    return response_result(1, build_jwt(user))


@router.get("/renew-token")
async def renew_token(request: Request):
    token = request.headers["Authorization"].replace("Bearer ", "")
    data = decode_token(token, check_expire=False)
    user = await User.get(entity_id=data["entityId"])
    return response_result(1, build_jwt(user))
