import os

import dotenv

print("加载环境变量...")
dotenv.load_dotenv()


class Env:
    DEBUG = os.getenv("DEBUG", "TRUE") == "TRUE"

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", 5432)

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost/0")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    TOKEN_EXPIRE = os.getenv("TOKEN_EXPIRE", 60)  # default: 60 minutes

    TENCENT_APP_ID = os.getenv("TENCENT_APP_ID")
    TENCENT_SECRET_ID = os.getenv("TENCENT_SECRET_ID")
    TENCENT_SECRET_KEY = os.getenv("TENCENT_SECRET_KEY")

    FROM_ADDRESS = os.getenv("SMS_SENDER")
    TEMPLATE_ID = os.getenv("SMS_TEMPLATE_ID")
    TEMPLATE_ARG = os.getenv("SMS_TEMPLATE_ARG")
