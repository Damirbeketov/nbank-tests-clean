import pytest
import requests
import uuid


@pytest.mark.api
class TestTransferJunior:

    @pytest.mark.parametrize(
        "amount",
        [10000, 9999, 9999.1, 9999.01, 1, 0.01, 0.1]
    )
    def test_transfer_account_positive(self, amount):
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

        # Логинимся
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

        deposit_1 = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit",
            json={"id": account_1, "balance": 5000},
            headers={"Authorization": token}
        )
        assert deposit_1.status_code == 200

        deposit_2 = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit",
            json={"id": account_1, "balance": 5000},
            headers={"Authorization": token}
        )
        assert deposit_2.status_code == 200

        # Выполняем трансфер
        transfer_resp = requests.post(
            "http://localhost:4111/api/v1/accounts/transfer",
            json={
                "senderAccountId": account_1,
                "receiverAccountId": account_2,
                "amount": amount
            },
            headers={"Authorization": token}
        )
        assert transfer_resp.status_code == 200

        transfer = transfer_resp.json()

        #
        assert float(transfer["amount"]) == float(round(amount, 2))
        assert transfer["senderAccountId"] == account_1
        assert transfer["receiverAccountId"] == account_2
        assert transfer["message"] == "Transfer successful"

        tx_resp = requests.get(
            f"http://localhost:4111/api/v1/accounts/{account_2}/transactions",
            headers={"Authorization": token}
        )
        assert tx_resp.status_code == 200

        transactions = tx_resp.json()
        assert len(transactions) > 0

        tx = transactions[0]

        assert float(tx["amount"]) == float(round(amount, 2))
        assert tx["type"] == "TRANSFER_IN"
        assert tx["relatedAccountId"] == account_1