import bcrypt

from utils.reference import AbstractCreateAtModel, fields


class User(AbstractCreateAtModel):
    entity_id = fields.CharField(max_length=16, unique=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=255)

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())
