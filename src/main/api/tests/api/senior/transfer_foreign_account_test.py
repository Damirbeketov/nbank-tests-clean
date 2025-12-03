import pytest

@pytest.mark.api
class TestTransferForeignAccount:

    @pytest.mark.parametrize(
        "amount, expected_message",
        [
            (100.1, "Invalid transfer: insufficient funds or invalid accounts"),
            (100.01, "Invalid transfer: insufficient funds or invalid accounts"),
            (100.001, "Invalid transfer: insufficient funds or invalid accounts"),
        ]
    )
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_transfer_negative(self, api_manager, user_request, amount, expected_message):
        api_manager.user_steps.login(user_request)
        account_1 = api_manager.user_steps.create_account(user_request)
        account_2 = api_manager.user_steps.create_account(user_request)
        api_manager.user_steps.deposit_account(user_request, account_1.id, 100)
        api_manager.user_steps.transfer_account_negative(
            user_request,
            account_1.id,
            account_2.id,
            amount,
            expected_message
        )

        # Проверяем, что состояние НЕ изменилось
        transactions = api_manager.user_steps.get_account_transactions(
            user_request,
            account_2.id
        )
        assert len(transactions) == 0