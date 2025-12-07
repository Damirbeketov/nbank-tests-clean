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
class TestTransferForeignAccountMiddle:

    @pytest.mark.parametrize(
        "amount, expected_message",
        [
            (100.1,  "Invalid transfer: insufficient funds or invalid accounts"),
            (100.01, "Invalid transfer: insufficient funds or invalid accounts"),
            (100.001, "Invalid transfer: insufficient funds or invalid accounts"),
        ]
    )
    def test_transfer_negative(self, amount, expected_message):
        username = RandomData.get_username()
        password = RandomData.get_password()
        user = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user)

        account_1 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        account_2 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_1.id, balance=100))

        response = TransferRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.bad_request_text(expected_message)
        ).post(TransferRequest(
            senderAccountId=account_1.id,
            receiverAccountId=account_2.id,
            amount=amount
        ))

        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get(account_2.id)

        assert len(transactions) == 0