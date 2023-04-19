import orjson

from utils.redis_agent import RedisSession
from .models import Room, RoomUser


class AbstractManager:
    session = RedisSession
    model = None

    @property
    def pre(self):
        return self.model.__name__

    def get(self, pk, to_object=True):
        if content := self.session.get(f"{self.pre}:{pk}"):
            data = orjson.loads(content)
            if to_object:
                return self.model.from_json(pk, data)
            else:
                return data

    def save(self, item):
        content = orjson.dumps(item.to_json())
        self.session.set(f"{self.pre}:{item.pk}", content)

    def delete(self, item):
        self.session.delete(f"{self.pre}:{item.pk}")

    def all(self, to_object=True):
        for key in self.session.scan_iter(f"{self.pre}:*"):
            _, pk = key.split(":")
            yield self.get(pk, to_object)

    def filter(self, **kwargs):
        for item in self.all():
            if hasattr(item, "filter"):
                if item.filter(**kwargs):
                    yield item
            else:
                yield item

    def has(self, pk):
        return self.session.exists(f"{self.pre}:{pk}")


class RoomManager(AbstractManager):
    model = Room


class RoomUserManager(AbstractManager):
    model = RoomUser


Room.objects = RoomManager()
RoomUser.objects = RoomUserManager()
