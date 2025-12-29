import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


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
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_deposit_negative(self, api_manager: ApiManager, user_request: CreateUserRequest,balance, expected_error):
        api_manager.user_steps.login(user_request)
        account = api_manager.user_steps.create_account(user_request)
        api_manager.user_steps.deposit_account_negative(
            user_request, account.id, balance, expected_error
        )

        # проверяем, что состояние НЕ изменилось
        transactions = api_manager.user_steps.get_account_transactions(
            user_request, account.id
        )

        assert len(transactions) == 0