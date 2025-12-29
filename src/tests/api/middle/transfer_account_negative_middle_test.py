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
class TestTransferNegativeMiddle:

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
    def test_transfer_negative(self, amount, expected_message):
        username = RandomData.get_username()
        password = RandomData.get_password()
        user_request = CreateUserRequest(username=username, password=password, role="USER")

        # добавляем юзера
        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        # создаём аккаунты
        account_1 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        account_2 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        # депозит
        DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_1.id, balance=5000))

        # вызываем трансфер
        TransferRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.bad_request_text(expected_message)
        ).post(TransferRequest(
            senderAccountId=account_1.id,
            receiverAccountId=account_2.id,
            amount=amount
        ))

        # проверяем, что состояние не изменилось
        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get(account_2.id)

        assert len(transactions) == 0