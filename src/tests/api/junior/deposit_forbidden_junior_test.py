import pytest
import requests
import uuid


@pytest.mark.api
class TestDepositForbiddenJunior:

    @pytest.mark.parametrize(
        "balance, expected_error",
        [
            (1000, "Unauthorized access to account"),
        ]
    )
    def test_deposit_forbidden(self, balance, expected_error):
        # создаём user1
        user1_resp = requests.post(
            'http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"user1_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user1_resp.status_code == 201
        user1 = user1_resp.json()["username"]

        # логин user1
        login1 = requests.post(
            'http://localhost:4111/api/v1/auth/login',
            json={"username": user1, "password": "Pass123!"}
        )
        token1 = login1.headers["authorization"]

        # создаём аккаунт user1
        acc1_resp = requests.post(
            'http://localhost:4111/api/v1/accounts',
            headers={"Authorization": token1}
        )
        assert acc1_resp.status_code == 201
        account1_id = acc1_resp.json()["id"]

        # создаём user2
        user2_resp = requests.post(
            'http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"user2_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user2_resp.status_code == 201
        user2 = user2_resp.json()["username"]

        # логин user2
        login2 = requests.post(
            'http://localhost:4111/api/v1/auth/login',
            json={"username": user2, "password": "Pass123!"}
        )
        token2 = login2.headers["authorization"]

        # создаём аккаунт user2
        requests.post(
            'http://localhost:4111/api/v1/accounts',
            headers={"Authorization": token2}
        )

        deposit = requests.post(
            'http://localhost:4111/api/v1/accounts/deposit',
            json={"id": account1_id, "balance": balance},
            headers={"Authorization": token2}
        )

        assert deposit.status_code == 403
        assert expected_error in deposit.text

        # проверяем что транзакций у user1 НЕТ
        tx_resp = requests.get(
            f'http://localhost:4111/api/v1/accounts/{account1_id}/transactions',
            headers={"Authorization": token1}
        )

        assert tx_resp.status_code == 200
        transactions = tx_resp.json()
        assert len(transactions) == 0

    def test_deposit_account_not_found(self):
        user_resp = requests.post(
            'http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"user_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user_resp.status_code == 201
        username = user_resp.json()["username"]

        login = requests.post(
            'http://localhost:4111/api/v1/auth/login',
            json={"username": username, "password": "Pass123!"}
        )
        token = login.headers["authorization"]

        nonexistent_id = 999999999

        deposit = requests.post(
            'http://localhost:4111/api/v1/accounts/deposit',
            json={"id": nonexistent_id, "balance": 1000},
            headers={"Authorization": token}
        )

        assert deposit.status_code == 403
        assert "Unauthorized access to account" in deposit.text


