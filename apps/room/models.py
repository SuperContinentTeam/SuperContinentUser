import json


class Room:
    PRE = "Room"

    def __init__(self, name, user_entity, room_entity, password=None, limit=20):
        self.name = name
        self.room_entity = room_entity
        self.user_entity = user_entity  # Room owner
        self.password = password
        self.limit = limit

    @property
    def key(self):
        return f"{self.PRE}:{self.room_entity}"

    def to_json(self):
        return {
            "name": self.name,
            "limit": self.limit,
            "password": self.password,
            "userEntity": self.user_entity
        }

    async def save(self, redis):
        # default save 3 minutes
        content = json.dumps(self.to_json(), ensure_ascii=False)
        redis.setex(self.key, 180, content)

    @classmethod
    def from_str(cls, room_entity, content):
        if content:
            data = json.loads(content)
            room = Room(
                name=data["name"],
                user_entity=data["userEntity"],
                password=data["password"],
                limit=data["limit"],
                room_entity=room_entity
            )
            return room

    async def delete(self, redis):
        await redis.client.delete(self.key)


class RoomUser:
    PRE = "RoomUser"

    def __init__(self, room_entity, user_entity):
        self.room_entity = room_entity
        self.user_entity = user_entity

    def to_json(self):
        return {}

    @property
    def key(self):
        return f"{self.PRE}:{self.room_entity}-{self.user_entity}"

    @staticmethod
    def from_str(key: str, content: str):
        _, temp = key.split(":")
        room_entity, user_entity = temp.split("-")
        return RoomUser(room_entity, user_entity)

    async def save(self, redis):
        content = json.dumps(self.to_json(), ensure_ascii=False)
        redis.set(self.key, content)

    @staticmethod
    async def iter(room_entity, redis):
        for key in redis.scan_iter(f"{RoomUser.PRE}:{room_entity}-*"):
            content = redis.get(key)
            yield RoomUser.from_str(key, content)

    async def delete(self, redis):
        redis.delete(self.key)
