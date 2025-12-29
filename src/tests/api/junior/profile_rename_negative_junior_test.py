import pytest
import requests
import uuid


@pytest.mark.api
class TestProfileRenameNegativeJunior:

    @pytest.mark.parametrize(
        "name, expected_message",
        [
            ('UserName', 'Name must contain two words with letters only'),
            ('User! Name', 'Name must contain two words with letters only'),
            ('User Name1', 'Name must contain two words with letters only'),
            ('user name.', 'Name must contain two words with letters only'),
            ('User', 'Name must contain two words with letters only'),
            ('User Name User', 'Name must contain two words with letters only'),
            (' User Name', 'Name must contain two words with letters only'),
            ('User Name ', 'Name must contain two words with letters only'),
            (' User Name ', 'Name must contain two words with letters only'),
            ('', 'Name must contain two words with letters only'),
            (' ', 'Name must contain two words with letters only'),
            ('! ?', 'Name must contain two words with letters only'),
        ]
    )
    def test_profile_rename_negative(self, name, expected_message):
        response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"user_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert response.status_code == 201
        username = response.json()["username"]

        # 2. Логинимся
        login_response = requests.post(
            url='http://localhost:4111/api/v1/auth/login',
            json={"username": username, "password": "Pass123!"}
        )
        assert login_response.status_code == 200
        token = login_response.headers["authorization"]

        profile_before = requests.get(
            url='http://localhost:4111/api/v1/customer/profile',
            headers={"Authorization": token}
        )
        assert profile_before.status_code == 200
        old_name = profile_before.json()["name"]

        rename_resp = requests.put(
            url='http://localhost:4111/api/v1/customer/profile',
            json={"name": name},
            headers={"Authorization": token}
        )

        assert rename_resp.status_code == 400
        assert rename_resp.text.strip() == expected_message

        profile_after = requests.get(
            url='http://localhost:4111/api/v1/customer/profile',
            headers={"Authorization": token}
        )
        assert profile_after.status_code == 200
        assert profile_after.json()["name"] == old_name