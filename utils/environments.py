import os

import dotenv

print("加载环境变量...")
dotenv.load_dotenv()


class Env:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", 5432)
