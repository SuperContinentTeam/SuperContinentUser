from aioredis import Redis
from fastapi import APIRouter, Request, Depends

from apps.room.interface import get_users_from_room
from apps.room.models import Room, RoomUser
from apps.user.reference import response_result
from utils.reference import random_string
from utils.redis_agent import get_redis_pool

router = APIRouter(prefix="/room")


@router.get("/list")
async def room_list(redis: Redis = Depends(get_redis_pool)):
    result = [
        Room.from_str(key.split(":")[-1], await redis.get(key)).to_json()
        for key in await redis.scan_iter(f"{Room.PRE}:*")
    ]
    return response_result(1, [room.to_json() for room in result])


@router.post("/create")
async def create_room(request: Request, redis: Redis = Depends(get_redis_pool)):
    body = await request.json()

    room_entity = random_string(16)
    while await redis.exists(f"{Room.PRE}:{room_entity}"):
        room_entity = random_string(16)

    room = Room(
        name=body["name"],
        limit=body.get("limit", 20),
        password=body.get("password"),
        user_entity=body["userEntity"],
        room_entity=room_entity
    )
    await room.save(redis)

    return response_result(1, room.to_json())


@router.get("/join/{room_entity}/{user_entity}")
async def user_join_room(user_entity, room_entity, redis: Redis = Depends(get_redis_pool)):
    if not await redis.exists(room_key := f"{Room.PRE}:{room_entity}"):
        return response_result(0, "Room not found")

    room = Room.from_str(room_entity, await redis.get(room_key))

    user_dict = await get_users_from_room(room_entity, redis)

    if len(user_dict) == room.limit:
        return response_result(0, "Room is full")

    if user_entity in user_dict:
        return response_result(0, "Already in the room")

    await RoomUser(room_entity, user_entity).save(redis)

    return response_result(1, "success")


@router.get("/leave/{room_entity}/{user_entity}")
async def user_leave_room(user_entity, room_entity, redis: Redis = Depends(get_redis_pool)):
    if await redis.exists(f"{Room.PRE}:{room_entity}"):
        user_dict = await get_users_from_room(room_entity, redis)
        if room_user := user_dict.get(user_entity):
            await room_user.delete(redis)
            del user_dict[room_user]

    return response_result(1, "success")


@router.get("/list/{room_entity}")
async def list_room_user(room_entity, redis: Redis = Depends(get_redis_pool)):
    if not await redis.exists(f"{Room.PRE}:{room_entity}"):
        return response_result(0, "Room not found")

    user_dict = await get_users_from_room(room_entity, redis)
    return response_result(1, {user_entity: user.to_json() for user_entity, user in user_dict.items()})
