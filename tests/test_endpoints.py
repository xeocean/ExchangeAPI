import asyncio
import random
import string
import pytest
from fastapi.testclient import TestClient
from app.db.database import init_db
from main import app

client = TestClient(app)
asyncio.run(init_db())


def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


@pytest.fixture
def valid_user_data():
    return {
        "username": generate_random_string(),
        "password": generate_random_string()
    }


@pytest.fixture
def token(valid_user_data):
    client.post("/auth/register", json=valid_user_data)
    response = client.post("/auth/login", data=valid_user_data)
    return response.json()["access_token"]


class TestAuth:

    def test_register_correct_data(self, valid_user_data):
        response = client.post("/auth/register", json=valid_user_data)
        assert response.status_code == 200
        assert "message" in response.json()

    def test_register_duplicate_username(self, valid_user_data):
        client.post("/auth/register", json=valid_user_data)
        response = client.post("/auth/register", json=valid_user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Username exists"

    def test_login_correct_data(self, valid_user_data):
        client.post("/auth/register", json=valid_user_data)
        response = client.post("/auth/login", data=valid_user_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_incorrect_password(self, valid_user_data):
        client.post("/auth/register", json=valid_user_data)
        response = client.post("/auth/login", data={
            "username": valid_user_data["username"],
            "password": "password"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect password"


class TestCurrency:

    def test_currency_codes(self, token):
        response = client.get("/currency/list", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["Currency codes"]

    def test_currency_translation(self, token):
        currency_data = {
            "value_1": "USD",
            "value_2": "RUB",
            "quantity": 10
        }
        response = client.post("/currency/exchange", json=currency_data, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert "message" in response.json()

    def test_currency_translation_invalid_code(self, token):
        currency_data = {
            "value_1": "INVALID",
            "value_2": "EUR",
            "quantity": 10
        }
        response = client.post("/currency/exchange", json=currency_data, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 422

    def test_currency_translation_unauthorized(self):
        currency_data = {
            "value_1": "USD",
            "value_2": "EUR",
            "quantity": 10
        }
        response = client.post("/currency/exchange", json=currency_data)
        assert response.status_code == 401
