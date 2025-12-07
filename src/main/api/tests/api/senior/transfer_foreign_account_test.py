import pytest

@pytest.mark.api
class TestTransferForeignAccount:

    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_transfer_negative(self, api_manager, user_request, deposit_amount, invalid_amount):
        api_manager.user_steps.login(user_request)

        account_1 = api_manager.user_steps.create_account(user_request)
        account_2 = api_manager.user_steps.create_account(user_request)
        api_manager.user_steps.deposit_account(user_request, account_1.id, deposit_amount)

        # Пробуем перевести сумму, превышающую баланс
        api_manager.user_steps.transfer_foreign_account_negative(
            user_request,
            account_1.id,
            account_2.id,
            invalid_amount
        )

        # Проверяем, что перевод НЕ создал транзакций
        transactions = api_manager.user_steps.get_account_transactions(user_request, account_2.id)

        assert len(transactions) == 0