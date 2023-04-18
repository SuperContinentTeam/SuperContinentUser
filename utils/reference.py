import random
import string

from fastapi.requests import Request
from tortoise import fields
from tortoise.models import Model


class AbstractBaseModel(Model):
    id: int = fields.IntField(pk=True)

    class Meta:
        abstract = True


class AbstractCreateAtModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


def try_to_do(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return True, result
        except Exception as e:
            print(e)
            return False, str(e)

    return inner


def random_string(length=6, digits=True):
    chars = string.ascii_letters + (string.digits if digits else "")
    return "".join(random.sample(chars, length))


async def parser_body(request: Request):
    return await request.json()
