import pytest, requests
import uuid


@pytest.mark.api
class TestDepositNegative:

    @pytest.mark.parametrize(
        "balance, expected_error",
        [
            (0, "Deposit amount must be at least 0.01"),
            (-1, "Deposit amount must be at least 0.01"),
            (-100, "Deposit amount must be at least 0.01"),
            (-0.1, "Deposit amount must be at least 0.01"),
            (5001, "Deposit amount cannot exceed 5000"),
            (5000.1, "Deposit amount cannot exceed 5000"),
            (5000.01, "Deposit amount cannot exceed 5000"),
            (5000.001, "Deposit amount cannot exceed 5000"),
        ]
    )
    def test_deposit_invalid(self, balance, expected_error):

        # создаём пользователя
        response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                "username": f"alex_{uuid.uuid4().hex[:6]}",
                "password": "Maks1995!",
                "role": "USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": "Basic YWRtaW46YWRtaW4="
            }
        )
        assert response.status_code == 201
        username = response.json()["username"]

        # логинимся
        login_response = requests.post(
            url='http://localhost:4111/api/v1/auth/login',
            json={"username": username, "password": "Maks1995!"}
        )
        assert login_response.status_code == 200
        token = login_response.headers["authorization"]

        # создаём аккаунт
        account_response = requests.post(
            url='http://localhost:4111/api/v1/accounts',
            headers={"Authorization": token}
        )
        assert account_response.status_code == 201
        account_id = account_response.json()["id"]

        # отправляем НЕ валидный депозит
        deposit_response = requests.post(
            url='http://localhost:4111/api/v1/accounts/deposit',
            json={"id": account_id, "balance": balance},
            headers={"Authorization": token}
        )

        assert deposit_response.status_code == 400
        actual_error = deposit_response.text.strip()
        assert actual_error == expected_error

        transactions_response = requests.get(
            url=f'http://localhost:4111/api/v1/accounts/{account_id}/transactions',
            headers={"Authorization": token}
        )

        assert transactions_response.status_code == 200
        transactions = transactions_response.json()
        assert transactions == []