from .models import RoomUser


async def get_users_from_room(room_entity):
    return {
        room_user.user_entity: room_user
        for room_user in await RoomUser.iter(room_entity)
    }
