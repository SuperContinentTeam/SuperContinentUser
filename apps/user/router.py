from fastapi import APIRouter
from fastapi.requests import Request

from apps.user.reference import send_and_stash_code

router = APIRouter(prefix="/user")


@router.post("/send-code")
async def send_code(request: Request):
    body = await request.json()
    print(body)
    code = send_and_stash_code(body["recipient"])
    return code
