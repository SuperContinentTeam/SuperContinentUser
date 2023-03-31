from fastapi import APIRouter
from fastapi.requests import Request

from utils.sms import SmsSender

router = APIRouter(prefix="/user")


@router.post("/send-code")
async def send_code(request: Request):
    body = await request.json()
    recipient = body["recipient"]

