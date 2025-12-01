import pytest
import requests
import uuid


@pytest.mark.api
class TestTransferNegativeJunior:

    @pytest.mark.parametrize(
        "amount, expected_error",
        [
            (-1, "Transfer amount must be at least 0.01"),
            (0, "Transfer amount must be at least 0.01"),
            (-0.1, "Transfer amount must be at least 0.01"),
            (10001, "Transfer amount cannot exceed 10000"),
            (10000.1, "Transfer amount cannot exceed 10000"),
            (10000.01, "Transfer amount cannot exceed 10000"),
        ]
    )
    def test_transfer_negative(self, amount, expected_error):
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

        # Создаём два счёта
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
            json={"id": account_1, "balance": 5000},
            headers={"Authorization": token}
        )
        assert deposit_resp.status_code == 200

        # Пытаемся выполнить transfer
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
        assert expected_error in transfer_resp.text

        tx_resp = requests.get(
            f"http://localhost:4111/api/v1/accounts/{account_2}/transactions",
            headers={"Authorization": token}
        )

        assert tx_resp.status_code == 200
        transactions = tx_resp.json()
        assert len(transactions) == 0