import importlib

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from jwt import PyJWTError
from tortoise.contrib.fastapi import register_tortoise

from apps.user.interface import decode_token
from apps.user.models import User
from utils.settings import *
from utils.whitelist import check_whitelist

app = FastAPI(default_response_class=ORJSONResponse)

# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

for app_name in BASE_DIR.joinpath("apps").iterdir():
    name = app_name.name
    if app_name.is_dir() and name != "__pycache__":
        print("导入应用: ", name)
        # 导入 Router
        try:
            r = importlib.import_module(f"apps.{name}.router")
            app.include_router(r.router)
        except Exception as e:
            print(f"未找到路由表: apps.{name}.router: {e}")

        # 导入 Signals
        if app_name.joinpath("signals.py").exists():
            importlib.import_module(f"apps.{name}.signals")


# http 拦截器
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if Env.DEBUG or check_whitelist(request.url.path):
        return await call_next(request)

    if not (token := request.headers.get("Authorization")):
        return Response("Token not found", status_code=400)

    token = token.replace("Bearer ", "")
    try:
        data = decode_token(token)
    except PyJWTError:
        return Response("Invalid token, expired", status_code=400)

    user = await User.filter(entity_id=data["entityId"]).first()
    request.scope["user"] = user

    return await call_next(request)


# 所有应用的model注册到数据库
register_tortoise(
    app,
    config={
        "connections": DATABASE,
        "apps": {"models": {"models": DATABASE_MODELS}},
        "use_tz": True,
        "timezone": "Asia/Shanghai",
    },
    generate_schemas=True,
)


@app.get("/health")
async def health():
    return "Health"
