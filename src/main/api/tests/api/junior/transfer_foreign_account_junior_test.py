import pytest
import requests
import uuid


@pytest.mark.api
class TestTransferForeignAccountJunior:

    @pytest.mark.parametrize(
        "amount, expected_message",
        [
            (100.1, "Invalid transfer: insufficient funds or invalid accounts"),
            (100.01, "Invalid transfer: insufficient funds or invalid accounts"),
            (100.001, "Invalid transfer: insufficient funds or invalid accounts"),
        ]
    )
    def test_transfer_negative(self, amount, expected_message):
        # 1. Создаём пользователя
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

        # 2. Логинимся
        login_resp = requests.post(
            "http://localhost:4111/api/v1/auth/login",
            json={"username": username, "password": "Pass123!"}
        )
        assert login_resp.status_code == 200
        token = login_resp.headers["authorization"]

        # 3. Создаём два аккаунта
        acc1_resp = requests.post(
            "http://localhost:4111/api/v1/accounts",
            headers={"Authorization": token}
        )
        assert acc1_resp.status_code == 201
        account_1 = acc1_resp.json()["id"]

        acc2_resp = requests.post(
            "http://localhost:4111/api/v1/accounts",
            headers={"Authorization": token}
        )
        assert acc2_resp.status_code == 201
        account_2 = acc2_resp.json()["id"]

        deposit_resp = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit",
            json={"id": account_1, "balance": 100},
            headers={"Authorization": token}
        )
        assert deposit_resp.status_code == 200

        transfer_resp = requests.post(
            "http://localhost:4111/api/v1/accounts/transfer",
            json={
                "senderAccountId": account_1,
                "receiverAccountId": account_2,
                "amount": amount
            },
            headers={"Authorization": token}
        )
        assert transfer_resp.status_code == 400
        assert expected_message in transfer_resp.text

        # 6. Проверяем, что транзакций НЕ появилось
        tx_resp = requests.get(
            f"http://localhost:4111/api/v1/accounts/{account_2}/transactions",
            headers={"Authorization": token}
        )
        assert tx_resp.status_code == 200

        transactions = tx_resp.json()
        assert len(transactions) == 0