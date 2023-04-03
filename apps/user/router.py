from fastapi import APIRouter
from fastapi.requests import Request

from utils.reference import random_string
from .reference import send_and_stash_code, response_result, check_code
from .models import User

router = APIRouter(prefix="/user")


@router.post("/send-code")
async def send_code(request: Request):
    body = await request.json()
    code = send_and_stash_code(body["recipient"])
    return code


@router.post("/register")
async def register(request: Request):
    body = await request.json()
    if await User.filter(username=body["username"]).exists():
        return response_result(2, "This username has been registered")
    if await User.filter(email=body["email"]).exists():
        return response_result(3, "This email has been registered")

    status, result = check_code(body["email"], body["code"])
    if not status or not result:
        return response_result(4, "Verification code has expired")

    entity_id = random_string(8)
    while await User.filter(entity_id=entity_id).exists():
        entity_id = random_string(8)

    user = User(entity_id=entity_id, username=body["username"], email=body["email"])
    user.set_password(body["password"])
    await user.save()

    return response_result(1, user)
