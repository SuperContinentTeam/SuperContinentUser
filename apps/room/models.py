class AbstractModel:
    objects = None

    def save(self):
        self.objects.save(self)

    def delete(self):
        self.objects.delete(self)


class Room(AbstractModel):
    objects = None

    def __init__(self, name, user_entity, room_entity, password=None, limit=20):
        self.name = name
        self.room_entity = room_entity
        self.user_entity = user_entity  # Room owner
        self.password = password
        self.limit = limit

    def to_json(self):
        return {
            "name": self.name,
            "limit": self.limit,
            "password": self.password,
            "userEntity": self.user_entity
        }

    @staticmethod
    def from_json(pk, data):
        return Room(data["name"], data["userEntity"], pk, data["password"], data["limit"])


class RoomUser(AbstractModel):
    objects = None

    def __init__(self, primary_key, room_entity, user_entity):
        self.pk = primary_key
        self.room_entity = room_entity
        self.user_entity = user_entity

    def to_json(self):
        return {
            "roomEntity": self.room_entity,
            "userEntity": self.user_entity
        }

    @staticmethod
    def from_json(pk, data):
        return RoomUser(pk, data["roomEntity"], data["userEntity"])

    def filter(self, **kwargs):
        if "room_entity" not in kwargs:
            return True

        return kwargs["room_entity"] == self.room_entity
