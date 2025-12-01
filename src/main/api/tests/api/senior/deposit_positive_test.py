import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDeposit:

    @pytest.mark.usefixtures('user_request', 'api_manager')
    def test_deposit(self, api_manager: ApiManager, user_request: CreateUserRequest):
        api_manager.user_steps.login(user_request)
        account = api_manager.user_steps.create_account(user_request)

        deposit = api_manager.user_steps.deposit_account(
            user_request,
            account.id,
            5000
        )

        assert deposit.balance == 5000
        assert deposit.id == account.id

        transactions = api_manager.user_steps.get_account_transactions(
            user_request, account.id
        )

        tx = transactions[0]

        assert tx.amount == 5000
        assert tx.type == "DEPOSIT"
        assert tx.relatedAccountId == account.id

    @pytest.mark.parametrize(
        "balance",
        [5000.00, 5000, 4999.99, 4999.999, 0.1, 1]
    )
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_deposit_positive(self, api_manager: ApiManager, user_request: CreateUserRequest, balance):

        api_manager.user_steps.login(user_request)
        account = api_manager.user_steps.create_account(user_request)

        deposit = api_manager.user_steps.deposit_account(
            user_request, account.id, balance
        )

        assert deposit.balance == balance
        assert deposit.id == account.id

        # Проверяем транзакции
        transactions = api_manager.user_steps.get_account_transactions(
            user_request, account.id
        )

        tx = transactions[0]

        assert tx.amount == balance
        assert tx.type == "DEPOSIT"
        assert tx.relatedAccountId == account.id