import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.steps.get_transactions_middle_requester import GetAccountTransactionsRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositMiddle:

    @pytest.mark.parametrize(
        "balance",
        [5000.00, 5000, 4999.99, 4999.999, 0.1, 1]
    )
    def test_deposit_positive(self, balance):

        # создаём юзера
        username = RandomData.get_username()
        password = RandomData.get_password()
        user_request = CreateUserRequest(username=username, password=password, role="USER")

        create_user_resp = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        # создаём аккаунт
        create_account_resp = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        account_id = create_account_resp.id

        # выполняем депозит
        deposit_resp = DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_id, balance=balance))

        assert float(deposit_resp.balance) == float(balance)

        # проверяем транзакции
        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get(account_id)

        assert len(transactions) == 1
        tx = transactions[0]

        assert float(tx.amount) == float(balance)
        assert tx.type == "DEPOSIT"
        assert tx.relatedAccountId == account_id