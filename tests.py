from fastapi.testclient import TestClient
import pytest
from contlika.asgi import app
from contlika.settings import API_V1_STR
from celestial.services import get_user_by_username
import logging
logger = logging.getLogger(__name__)

pytestmark = pytest.mark.django_db

client = TestClient(app)

@pytest.mark.django_db
def test_signup():
    user_details = {
        "device_id": "1234",
        "email": "test@example.com"
    }
    response = client.post(f"{API_V1_STR}/user/signup", json=user_details)
    assert response.status_code == 200
    assert response.json() == {"device_id": "1234"}

@pytest.mark.django_db
def test_login():
    user_details = {
        "device_id": "1234"
    }
    response = client.post(f"{API_V1_STR}/user/login", json=user_details)

    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']
    shown_name = response.json()['shown_name']
    assert response.status_code == 200
    assert response.json() == {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "shown_name": shown_name,
        "device_id": '1234',
        "queue": None
    }
    global TOKEN
    TOKEN = str(access_token)
    
    global AUTH
    AUTH = 'Bearer '+ TOKEN
    headers = {"Authorization": AUTH}
    
    response = client.get(f"{API_V1_STR}/user/get_my_posts")
    logger.info(AUTH)
    logger.info(response.json())
    # assert response.status_code == 307
    # assert response.json() == {}

# @pytest.mark.django_db
