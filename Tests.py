import base64
import json
from app import app as fl_app

import pytest
from pytest import *
import app
from json import *
import os
import tempfile

import pytest


@pytest.fixture
def app():
    yield fl_app


@pytest.fixture
def client(app):
    return app.test_client()


class TestUser:
    def test_user_create(self, client):
        temp = {
            "username": "Untouchable",
            "firstName": "Untouchable",
            "lastName": "Untouchable",
            "phone": "88005553535",
            "email": "post@post.xyz",
            "password": "2135114"
        }

        temp = json.dumps(temp)

        response = client.post('http://localhost:5000/user',
                               headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                               data=temp)

        assert response.status_code == 200

    def test_get_user_by_id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        response = client.get("http://localhost:5000/user/1", headers={"Authorization": f"Bearer {temp}"})
        assert response.status_code == 200


    def test_user_not_found_id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        response = client.get("http://localhost:5000/user/-1", headers={"Authorization": f"Bearer {temp}"})
        assert response.status_code == 404


    def test_login(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        # TestUser.temp_token += response.data
        assert response.status_code == 200

    def test_wrong_pass_login(self, client):
        credentials = base64.b64encode(b"Voavn:213511qweqw4").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        # TestUser.temp_token += response.data
        assert response.status_code == 401

    def test_wrong_login_in_login(self, client):
        credentials = base64.b64encode(b"Voavn:213511qweqw4").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        # TestUser.temp_token += response.data
        assert response.status_code == 401

    def test_get_users(self, client):
        response = client.get('http://localhost:5000/user')
        assert response.status_code == 200


    def test_phone_upd_user_by_Id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        data_t = {
            'firstName': 'NEw',
            'lastName': 'NEwee',
            'email': 'NEw',
            'phone': '88005553535'
        }
        data_t = json.dumps(data_t)
        response = client.put("http://localhost:5000/user/1",
                              headers={'Authorization': f"Bearer {temp}", 'Content-Type': 'application/json'},
                              data=data_t)
        assert response.status_code == 200

    def test_upd_user_by_Id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        data_t = {
            'firstName': 'NEw',
            'lastName': 'NEwee',
            'email': 'NEw',
            'phone': '88005553535'
        }
        data_t = json.dumps(data_t)
        response = client.put("http://localhost:5000/user/1",
                              headers={'Authorization': f"Bearer {temp}", 'Content-Type': 'application/json'},
                              data=data_t)
        assert response.status_code == 200




    # def test_delete_user_by_Id(self, client):
    #     credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
    #     response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
    #     temp = response.json
    #
    #
    #     response = client.delete("http://localhost:5000/user/1", headers={'Authorization': f"Bearer {temp}"})
    #     assert response.status_code == 200

class TestStudent:
    def test_student_create(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json

        temp2 = {
            "name": "Untouchable",
            "lastName": "Untouchable",
            "avarageMark": "4",
            "User_id": "22"
        }

        temp2 = json.dumps(temp2)

        response = client.post('http://localhost:5000/student',
                               headers={'Content-Type': 'application/json','Authorization': f"Bearer {temp}", 'Accept': 'application/json'},
                               data=temp2)

        assert response.status_code == 200

    def test_get_student_by_id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        response = client.get("http://localhost:5000/student/10", headers={"Authorization": f"Bearer {temp}"})
        assert response.status_code == 200

    def test_student_not_found_by_id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        response = client.get("http://localhost:5000/student/-1", headers={"Authorization": f"Bearer {temp}"})
        assert response.status_code == 404


    def test_upd_student_by_Id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json
        data_t = {
            'name': 'NEw',
            'lastName': 'NEwee',
            'avarageMark': '2'
        }
        data_t = json.dumps(data_t)
        response = client.put("http://localhost:5000/student/10",
                              headers={'Authorization': f"Bearer {temp}", 'Content-Type': 'application/json'},
                              data=data_t)

        assert response.status_code == 200

    def test_delete_student_denied_by_Id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json

        response = client.delete("http://localhost:5000/student/14", headers={'Authorization': f"Bearer {temp}"})
        assert response.status_code == 401

    def test_delete_student_by_Id(self, client):
        credentials = base64.b64encode(b"Voavn:2135114").decode('utf-8')
        response = client.get("http://localhost:5000/login", headers={"Authorization": f"Basic {credentials}"})
        temp = response.json

        response = client.delete("http://localhost:5000/student/5", headers={'Authorization': f"Bearer {temp}"})
        assert response.status_code == 200




    def test_duplicate_key(self, client):
        assert 1 == 1
