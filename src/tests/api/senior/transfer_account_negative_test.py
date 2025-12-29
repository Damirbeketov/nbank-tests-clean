import pytest


@pytest.mark.api
class TestTransferAccount:

    @pytest.mark.parametrize(
        "amount, expected_message",
        [
            (-1, "Transfer amount must be at least 0.01"),
            (0, "Transfer amount must be at least 0.01"),
            (-0.1, "Transfer amount must be at least 0.01"),
            (10001, "Transfer amount cannot exceed 10000"),
            (10000.1, "Transfer amount cannot exceed 10000"),
            (10000.01, "Transfer amount cannot exceed 10000"),
        ]
    )
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_transfer_negative(self, api_manager, user_request, amount, expected_message):
        api_manager.user_steps.login(user_request)
        account_1 = api_manager.user_steps.create_account(user_request)
        account_2 = api_manager.user_steps.create_account(user_request)
        api_manager.user_steps.deposit_account(user_request, account_1.id, 5000)
        api_manager.user_steps.transfer_account_negative(
            user_request,
            account_1.id,
            account_2.id,
            amount,
            expected_message
        )

        # Проверяем, что состояние НЕ изменилось
        transactions = api_manager.user_steps.get_account_transactions(user_request, account_2.id)
        assert len(transactions) == 0