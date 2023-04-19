from fastapi import APIRouter, Depends

from apps.room.models import Room, RoomUser
from apps.user.reference import response_result, parse_body
from utils.reference import random_string

router = APIRouter(prefix="/room")


@router.get("/list")
async def room_list():
    return response_result(1, [i for i in Room.objects.all(to_object=False)])


@router.post("/create")
async def create_room(body: dict = Depends(parse_body)):
    room_entity = random_string(16)
    while Room.objects.has(room_entity):
        room_entity = random_string(16)

    room = Room(
        name=body["name"],
        limit=body.get("limit", 20),
        password=body.get("password"),
        user_entity=body["userEntity"],
        room_entity=room_entity
    )

    room.objects.save()

    return response_result(1, room.to_json())


@router.get("/join/{room_entity}/{user_entity}")
async def user_join_room(user_entity, room_entity):
    if not Room.objects.has(room_entity):
        return response_result(0, "Room not found")

    room = Room.objects.get(room_entity)

    users = {user.user_entity: user for user in RoomUser.objects.filter(room_entity=room_entity)}

    if len(users) == room.limit:
        return response_result(0, "Room is full")

    if user_entity in users:
        return response_result(0, "Already in the room")

    RoomUser(f"{room_entity}:{user_entity}", room_entity, user_entity).save()

    return response_result(1, "success")


@router.get("/leave/{room_entity}/{user_entity}")
async def user_leave_room(user_entity, room_entity):
    if Room.objects.has(room_entity):
        users = {user.user_entity: user for user in RoomUser.objects.filter(room_entity=room_entity)}

        if room_user := users.get(user_entity):
            room_user.delete()

    return response_result(1, "success")


@router.get("/list/{room_entity}")
async def list_room_user(room_entity):
    if not Room.objects.has(room_entity):
        return response_result(0, "Room not found")

    return response_result(1, {
        user.user_entity: user.to_json()
        for user in RoomUser.objects.filter(room_entity=room_entity)
    })
