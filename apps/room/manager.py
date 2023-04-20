import orjson

from utils.redis_agent import RedisSession


class Manager:
    session = RedisSession
    __instance = dict()

    def __new__(cls, model):
        name = model.__name__
        if name not in cls.__instance:
            cls.__instance[name] = object.__new__(cls)

        return cls.__instance[name]

    def __init__(self, model):
        self.model = model
        self.pre = model.__name__

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
        if isinstance(item, str):
            key = item
        else:
            key = item.pk

        self.session.delete(f"{self.pre}:{key}")

    def all(self, to_object=True):
        for key in self.session.scan_iter(f"{self.pre}:*"):
            _, *pk = key.split(":")
            yield self.get(":".join(pk), to_object)

    def filter(self, **kwargs):
        for item in self.all():
            if hasattr(item, "filter"):
                if item.filter(**kwargs):
                    yield item
            else:
                yield item

    def has(self, pk):
        return self.session.exists(f"{self.pre}:{pk}")
