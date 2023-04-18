import json


class RoomUser:
    def __init__(self, user_entity):
        self.user_entity = user_entity

    def encode(self):
        return json.dumps({
            "userEntity": self.user_entity
        }, ensure_ascii=False)

    @staticmethod
    def decode(content):
        d = json.loads(content)
        return RoomUser(
            user_entity=d["userEntity"]
        )


class Room:
    PRE = "Room"

    def __init__(self, name, user_entity, room_entity, password=None, limit=20):
        self.name = name
        self.user_entity = user_entity  # Room owner
        self.password = password
        self.limit = limit
        self.room_entity = room_entity
        self.user_list = []

    @property
    def key(self):
        return f"{self.PRE}:{self.room_entity}"

    def to_json(self):
        return {
            "name": self.name,
            "limit": self.limit,
            "password": self.password,
            "userEntity": self.user_entity,
            "userList": [user.encode() for user in self.user_list]
        }

    async def save(self, redis):
        # default save 3 minutes
        key = self.key
        content = json.dumps(self.to_json(), ensure_ascii=False)
        await redis.client.set(key, content)

    @classmethod
    def get_room(cls, room_entity, content):
        if content:
            data = json.loads(content)
            room = Room(
                name=data["name"],
                user_entity=data["userEntity"],
                password=data["password"],
                limit=data["limit"],
                room_entity=room_entity
            )
            room.user_list = [
                RoomUser.decode(i) for i in data["userList"]
            ]
            return room

    async def delete(self, redis):
        await redis.client.delete(self.key)
