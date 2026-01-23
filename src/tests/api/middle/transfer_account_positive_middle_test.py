import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.requests.steps.get_transactions_middle_requester import GetAccountTransactionsRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferMiddle:

    @pytest.mark.parametrize(
        "amount",
        [10000, 9999, 9999.1, 9999.01, 1, 0.01, 0.1]
    )
    def test_transfer_positive(self, amount):
        username = RandomData.get_username()
        password = RandomData.get_password()
        user_request = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        # создаём аккаунт 1
        account_1 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        # создаём аккаунт 2
        account_2 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        # депозит 1: +5000
        DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_1.id, balance=5000))

        # депозит 2: +5000
        DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_1.id, balance=5000))

        # выполняем трансфер
        transfer_resp = TransferRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(TransferRequest(
            senderAccountId=account_1.id,
            receiverAccountId=account_2.id,
            amount=amount
        ))

        # проверяем тело ответа
        assert float(transfer_resp.amount) == float(amount)
        assert transfer_resp.senderAccountId == account_1.id
        assert transfer_resp.receiverAccountId == account_2.id
        assert transfer_resp.message == "Transfer successful"

        # проверяем транзакцию в account_2 (получатель)
        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get(account_2.id)

        tx = transactions[0]

        assert float(tx.amount) == float(amount)
        assert tx.type == "TRANSFER_IN"
        assert tx.relatedAccountId == account_1.id