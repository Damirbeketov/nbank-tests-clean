import pytest
from src.main.api.models.transaction_type import TransactionType


@pytest.mark.api
class TestTransferAccount:
    @pytest.mark.parametrize(
        "amount",
        [10000, 9999, 9999.1, 9999.01, 1, 0.01, 0.1]
    )
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_transfer_account_positive(self, api_manager, user_request, amount):
        api_manager.user_steps.login(user_request)

        account_1 = api_manager.user_steps.create_account(user_request)
        account_2 = api_manager.user_steps.create_account(user_request)

        # Два пополнения по 5000
        api_manager.user_steps.repeat(
            2,
            api_manager.user_steps.deposit_account,
            user_request,
            account_1.id,
            5000
        )

        # Трансфер
        transfer = api_manager.user_steps.transfer_account(
            user_request,
            account_1.id,
            account_2.id,
            amount
        )

        assert transfer.amount == amount
        assert transfer.senderAccountId == account_1.id
        assert transfer.receiverAccountId == account_2.id
        assert transfer.message == 'Transfer successful'

        # Проверяем транзакции
        transactions = api_manager.user_steps.get_account_transactions(
            user_request, account_2.id
        )

        tx = transactions[0]

        assert tx.amount == amount
        assert tx.type == TransactionType.TRANSFER_IN
        assert tx.relatedAccountId == account_1.id

