import pytest
import requests
import uuid


@pytest.mark.api
class TestProfileRenameJunior:

    @pytest.mark.parametrize(
        "name",
        [
            "New Name",
            "new name",
            "Name new",
            "name New",
            "NEW NAME",
            "N N",
            "n n"
        ]
    )
    def test_profile_rename(self, name):
        user_resp = requests.post(
            "http://localhost:4111/api/v1/admin/users",
            json={
                "username": f"user_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user_resp.status_code == 201
        username = user_resp.json()["username"]

        login_resp = requests.post(
            "http://localhost:4111/api/v1/auth/login",
            json={"username": username, "password": "Pass123!"}
        )
        assert login_resp.status_code == 200
        token = login_resp.headers["authorization"]

        rename_resp = requests.put(
            "http://localhost:4111/api/v1/customer/profile",
            json={"name": name},
            headers={"Authorization": token}
        )
        assert rename_resp.status_code == 200

        rename = rename_resp.json()

        assert rename["customer"]["name"] == name
        assert rename["message"] == "Profile updated successfully"

        get_profile_resp = requests.get(
            "http://localhost:4111/api/v1/customer/profile",
            headers={"Authorization": token}
        )
        assert get_profile_resp.status_code == 200

        profile = get_profile_resp.json()
        assert profile["name"] == name