import datetime

import jwt

from utils.environments import Env

from .models import User


def build_jwt(user: User):
    data = {
        "entityId": user.entity_id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=Env.TOKEN_EXPIRE)
    }
    print(data)

    return jwt.encode(data, Env.SECRET_KEY, algorithm=Env.ALGORITHM)


def decode_token(token: str, check_expire=True):
    return jwt.decode(token, Env.SECRET_KEY, algorithms=[Env.ALGORITHM], options={"verify_exp": check_expire})
