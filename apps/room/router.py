from fastapi import APIRouter, Depends

from apps.room.interface import get_users_from_room
from apps.room.models import Room, RoomUser
from apps.user.reference import response_result, parse_body
from utils.redis_agent import RedisSession
from utils.reference import random_string

router = APIRouter(prefix="/room")


@router.get("/list")
async def room_list():
    result = [
        Room.from_str(key.split(":")[-1], RedisSession.get(key)).to_json()
        for key in RedisSession.scan_iter(f"{Room.PRE}:*")
    ]
    return response_result(1, [room.to_json() for room in result])


@router.post("/create")
async def create_room(body: dict = Depends(parse_body)):
    room_entity = random_string(16)
    while RedisSession.exists(f"{Room.PRE}:{room_entity}"):
        room_entity = random_string(16)

    room = Room(
        name=body["name"],
        limit=body.get("limit", 20),
        password=body.get("password"),
        user_entity=body["userEntity"],
        room_entity=room_entity
    )
    await room.save(RedisSession)

    return response_result(1, room.to_json())


@router.get("/join/{room_entity}/{user_entity}")
async def user_join_room(user_entity, room_entity):
    if not RedisSession.exists(room_key := f"{Room.PRE}:{room_entity}"):
        return response_result(0, "Room not found")

    room = Room.from_str(room_entity, RedisSession.get(room_key))

    user_dict = await get_users_from_room(room_entity)

    if len(user_dict) == room.limit:
        return response_result(0, "Room is full")

    if user_entity in user_dict:
        return response_result(0, "Already in the room")

    await RoomUser(room_entity, user_entity).save()

    return response_result(1, "success")


@router.get("/leave/{room_entity}/{user_entity}")
async def user_leave_room(user_entity, room_entity):
    if RedisSession.exists(f"{Room.PRE}:{room_entity}"):
        user_dict = await get_users_from_room(room_entity)
        if room_user := user_dict.get(user_entity):
            await room_user.delete(RedisSession)
            del user_dict[room_user]

    return response_result(1, "success")


@router.get("/list/{room_entity}")
async def list_room_user(room_entity):
    if not RedisSession.exists(f"{Room.PRE}:{room_entity}"):
        return response_result(0, "Room not found")

    user_dict = await get_users_from_room(room_entity)
    return response_result(1, {user_entity: user.to_json() for user_entity, user in user_dict.items()})
