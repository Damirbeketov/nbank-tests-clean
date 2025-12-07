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
class TestTransferBetweenUsersMiddle:
    def test_transfer_between_users(self):
        username1 = RandomData.get_username()
        password1 = RandomData.get_password()
        user1 = CreateUserRequest(username=username1, password=password1, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user1)

        username2 = RandomData.get_username()
        password2 = RandomData.get_password()
        user2 = CreateUserRequest(username=username2, password=password2, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user2)

        account_1 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username1, password1),
            ResponseSpecs.entity_was_created()
        ).post()

        account_2 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username2, password2),
            ResponseSpecs.entity_was_created()
        ).post()

        DepositRequester(
            RequestSpecs.auth_as_user(username1, password1),
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_1.id, balance=5000))


        transfer_resp = TransferRequester(
            RequestSpecs.auth_as_user(username1, password1),
            ResponseSpecs.request_returns_ok()
        ).post(TransferRequest(
            senderAccountId=account_1.id,
            receiverAccountId=account_2.id,
            amount=1000
        ))


        assert transfer_resp.amount == 1000.0
        assert transfer_resp.senderAccountId == account_1.id
        assert transfer_resp.receiverAccountId == account_2.id
        assert transfer_resp.message == "Transfer successful"

        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username2, password2),
            ResponseSpecs.request_returns_ok()
        ).get(account_2.id)

        tx = transactions[0]

        assert tx.amount == 1000.0
        assert tx.type == "TRANSFER_IN"
        assert tx.relatedAccountId == account_1.id