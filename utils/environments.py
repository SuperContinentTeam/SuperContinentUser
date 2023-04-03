import os

import dotenv

print("加载环境变量...")
dotenv.load_dotenv()


class Env:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", 5432)

    SMS_SENDER = os.getenv("SMS_SENDER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT", 25)
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_SELECT = os.getenv("REDIS_SELECT", 0)

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    TOKEN_EXPIRE = os.getenv("TOKEN_EXPIRE", 60)  # default: 60 minutes
