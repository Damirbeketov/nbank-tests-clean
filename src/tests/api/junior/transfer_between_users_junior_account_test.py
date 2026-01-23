import pytest
import requests
import uuid


@pytest.mark.api
class TestTransferBetweenUsersJunior:

    def test_transfer_between_users(self):
        user1_resp = requests.post(
            "http://localhost:4111/api/v1/admin/users",
            json={
                "username": f"user1_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user1_resp.status_code == 201
        user1 = user1_resp.json()["username"]

        # Логин user1
        login1 = requests.post(
            "http://localhost:4111/api/v1/auth/login",
            json={"username": user1, "password": "Pass123!"}
        )
        assert login1.status_code == 200
        token1 = login1.headers["authorization"]

        user2_resp = requests.post(
            "http://localhost:4111/api/v1/admin/users",
            json={
                "username": f"user2_{uuid.uuid4().hex[:6]}",
                "password": "Pass123!",
                "role": "USER"
            },
            headers={"Authorization": "Basic YWRtaW46YWRtaW4="}
        )
        assert user2_resp.status_code == 201
        user2 = user2_resp.json()["username"]

        # Логин user2
        login2 = requests.post(
            "http://localhost:4111/api/v1/auth/login",
            json={"username": user2, "password": "Pass123!"}
        )
        assert login2.status_code == 200
        token2 = login2.headers["authorization"]

        acc1_resp = requests.post(
            "http://localhost:4111/api/v1/accounts",
            headers={"Authorization": token1}
        )
        assert acc1_resp.status_code == 201
        account_1 = acc1_resp.json()["id"]

        acc2_resp = requests.post(
            "http://localhost:4111/api/v1/accounts",
            headers={"Authorization": token2}
        )
        assert acc2_resp.status_code == 201
        account_2 = acc2_resp.json()["id"]

        deposit_resp = requests.post(
            "http://localhost:4111/api/v1/accounts/deposit",
            json={"id": account_1, "balance": 5000},
            headers={"Authorization": token1}
        )
        assert deposit_resp.status_code == 200

        transfer_resp = requests.post(
            "http://localhost:4111/api/v1/accounts/transfer",
            json={
                "senderAccountId": account_1,
                "receiverAccountId": account_2,
                "amount": 1000
            },
            headers={"Authorization": token1}
        )
        assert transfer_resp.status_code == 200

        transfer = transfer_resp.json()

        assert transfer["amount"] == 1000
        assert transfer["senderAccountId"] == account_1
        assert transfer["receiverAccountId"] == account_2
        assert transfer["message"] == "Transfer successful"


        tx_resp = requests.get(
            f"http://localhost:4111/api/v1/accounts/{account_2}/transactions",
            headers={"Authorization": token2}
        )
        assert tx_resp.status_code == 200

        transactions = tx_resp.json()
        assert len(transactions) > 0

        tx = transactions[0]

        assert tx["amount"] == 1000
        assert tx["type"] == "TRANSFER_IN"
        assert tx["relatedAccountId"] == account_1