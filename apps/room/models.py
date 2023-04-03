import json

from utils.redis_agent import RedisSession
from utils.reference import random_string


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

    def __init__(self, name, user_entity, password=None, limit=20, room_entity=None):
        self.name = name
        self.user_entity = user_entity  # Room owner
        self.password = password
        self.limit = limit
        self.room_entity = room_entity or self.generate_entity()
        self.user_list = []

    def generate_entity(self):
        entity_id = random_string(8)
        while RedisSession.client.exists(f"{self.PRE}:{entity_id}"):
            entity_id = random_string(8)
        return entity_id

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

    def save(self):
        # default save 3 minutes
        key = self.key
        content = json.dumps(self.to_json(), ensure_ascii=False)
        RedisSession.client.set(key, content)

    @classmethod
    def get_room(cls, room_entity):
        key = f"{cls.PRE}:{room_entity}"
        content = RedisSession.client.get(key)
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

    def delete(self):
        RedisSession.client.delete(self.key)
