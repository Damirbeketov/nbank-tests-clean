import pytest

@pytest.mark.api
class TestDepositForbidden:

    @pytest.mark.parametrize(
        "balance, expected_error",
        [
            (1000, "Unauthorized access to account"),
        ]
    )
    def test_deposit_forbidden(self, balance, expected_error, api_manager, user_request_1, user_request_2):
        api_manager.user_steps.login(user_request_1)
        api_manager.user_steps.login(user_request_2)

        account_1 = api_manager.user_steps.create_account(user_request_1)
        api_manager.user_steps.create_account(user_request_2)

        deposit = api_manager.user_steps.deposit_account_forbidden(
            user_request_2, account_1.id, balance
        )

        assert expected_error in deposit.text

        transactions = api_manager.user_steps.get_account_transactions(user_request_1, account_1.id)
        assert len(transactions) == 0


    def test_deposit_account_not_found(self, api_manager, user_request):
        api_manager.user_steps.login(user_request)

        nonexistent_id = 999999999

        deposit = api_manager.user_steps.deposit_account_forbidden(
            user_request, nonexistent_id, 1000
        )

        assert "Unauthorized access to account" in deposit.text