from fastapi import APIRouter, Request

from apps.room.models import Room, RoomUser
from apps.user.reference import response_result

router = APIRouter(prefix="/room")


@router.get("/list")
async def room_list():
    return response_result(1, [
        Room.get_room(key.split(":")[-1]).to_json()
        for key in RedisSession.client.scan_iter("Room:*")
    ])


@router.post("/create")
async def create_room(request: Request):
    body = await request.json()
    room = Room(
        name=body["name"],
        limit=body.get("limit", 20),
        password=body.get("password"),
        user_entity=body["userEntity"]
    )
    room.user_list.append(RoomUser(user_entity=body["userEntity"]))
    room.save()
    return response_result(1, room.to_json())


@router.get("/join/{room_entity}/{user_entity}")
async def user_join_room(user_entity, room_entity):
    if not (room := Room.get_room(room_entity)):
        return response_result(0, "Room not found")

    if len(room.user_list) == room.limit:
        return response_result(0, "Room is full")

    for room_user in room.user_list:
        if room_user.user_entity == user_entity:
            return response_result(0, "Already in the room")

    room.user_list.append(RoomUser(user_entity=user_entity))
    room.save()
    return response_result(1, "success")


@router.get("/leave/{room_entity}/{user_entity}")
async def user_leave_room(user_entity, room_entity):
    if not (room := Room.get_room(room_entity)):
        return response_result(0, "Room not found")

    temp_list = []
    for room_user in room.user_list:
        if room_user.user_entity != user_entity:
            temp_list.append(room_user)

    room.user_list = temp_list
    room.save()
    return response_result(1, "success")
