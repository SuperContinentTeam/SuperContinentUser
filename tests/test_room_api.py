import unittest

from fastapi.testclient import TestClient
from main import app
from utils.reference import random_string


class TestRoomApi(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.cache = dict()

    def test_request(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn("code", data := response.json())
        self.assertEqual(data["code"], 1)
        return data

    def test_list_room(self):
        response = self.client.get("/room/list")
        self.test_request(response)

    def test_create_room(self):
        data = {
            "name": "HelloWorld",
            "userEntity": (user_entity := random_string()),
            "limit": 1
        }

        response = self.client.post("/room/create", json=data)
        body = self.test_request(response)
