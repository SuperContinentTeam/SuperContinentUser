from tortoise.models import Model
from tortoise import fields


class AbstractBaseModel(Model):
    id: int = fields.IntField(pk=True)

    class Meta:
        abstract = True


class AbstractCreateAtModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
