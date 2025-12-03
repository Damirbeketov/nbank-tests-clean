import pytest

from src.main.api.classes.api_manager import ApiManager


@pytest.mark.api
class TestTransferBetweenUsers:
    @pytest.mark.usefixtures("api_manager", "user_request_1", "user_request_2")
    def test_transfer_between_users(self, api_manager: ApiManager, user_request_1, user_request_2):
        api_manager.user_steps.login(user_request_1)
        api_manager.user_steps.login(user_request_2)
        account_1 = api_manager.user_steps.create_account(user_request_1)
        account_2 = api_manager.user_steps.create_account(user_request_2)
        api_manager.user_steps.deposit_account(user_request_1,account_1.id, amount=5000)
        transfer = api_manager.user_steps.transfer_account(
            user_request_1,
            account_1.id,
            account_2.id,
            amount=1000
        )

        assert transfer.amount == 1000.0
        assert transfer.senderAccountId == account_1.id
        assert transfer.receiverAccountId == account_2.id
        assert transfer.message == 'Transfer successful'

        # Проверяем транзакции
        transactions = api_manager.user_steps.get_account_transactions(
            user_request_2, account_2.id
        )

        tx = transactions[0]

        assert tx.amount == transfer.amount
        assert tx.type == "TRANSFER_IN"
        assert tx.relatedAccountId == account_1.id



