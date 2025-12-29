import pytest, requests
import uuid


@pytest.mark.api
class TestCreateAccount:

    @pytest.mark.debug
    @pytest.mark.parametrize(
        "balance",
        [5000.00, 5000, 4999.99, 4999.999, 0.1, 1]
    )
    def test_create_account(self, balance):
        response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"max_250_{uuid.uuid4().hex[:6]}",
                "password": "Maks1995!",
                "role": "USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic YWRtaW46YWRtaW4="
            }
        )
        assert response.status_code == 201
        user_name = response.json()["username"]

        # Логиним
        login_response = requests.post(
            url='http://localhost:4111/api/v1/auth/login',
            json={"username": user_name, "password": "Maks1995!"}
        )
        assert login_response.status_code == 200
        authorization_token = login_response.headers["authorization"]

        # Создаём счёт
        create_account_response = requests.post(
            url='http://localhost:4111/api/v1/accounts',
            headers={"Authorization": authorization_token}
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json()["balance"] == 0.0
        assert create_account_response.json()["transactions"] == []

        account_id = create_account_response.json()["id"]

        # Делаем депозит
        deposit_money_response = requests.post(
            url='http://localhost:4111/api/v1/accounts/deposit',
            json={"id": account_id, "balance": balance},
            headers={"Authorization": authorization_token}
        )
        assert deposit_money_response.status_code == 200
        assert deposit_money_response.json()["balance"] == float(balance)
        assert deposit_money_response.json()["id"] == account_id

        transactions_response = requests.get(
            url=f'http://localhost:4111/api/v1/accounts/{account_id}/transactions',
            headers={"Authorization": authorization_token}
        )

        assert transactions_response.status_code == 200

        transactions = transactions_response.json()
        assert len(transactions) == 1

        tx = transactions[0]
        assert tx["amount"] == float(balance)
        assert tx["type"] == "DEPOSIT"
        assert tx["relatedAccountId"] == account_id