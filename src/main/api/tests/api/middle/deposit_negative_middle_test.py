import pytest

from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.steps.get_transactions_middle_requester import GetAccountTransactionsRequester
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDepositNegativeMiddle:

    @pytest.mark.parametrize(
        "balance, expected_error",
        [
            (0, "Deposit amount must be at least 0.01"),
            (-1, "Deposit amount must be at least 0.01"),
            (-100, "Deposit amount must be at least 0.01"),
            (-0.1, "Deposit amount must be at least 0.01"),
            (5001, "Deposit amount cannot exceed 5000"),
            (5000.1, "Deposit amount cannot exceed 5000"),
            (5000.01, "Deposit amount cannot exceed 5000"),
            (5000.001, "Deposit amount cannot exceed 5000"),
        ]
    )
    def test_deposit_negative(self, balance, expected_error):

        # создаём юзера
        username = RandomData.get_username()
        password = RandomData.get_password()
        user_request = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        # создаём аккаунт
        create_account_resp = CreateAccountRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.entity_was_created()
        ).post()

        account_id = create_account_resp.id

        DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.bad_request_text(expected_error)
        ).post(DepositRequest(id=account_id, balance=balance))

        # проверяем, что транзакций нет
        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get(account_id)

        assert len(transactions) == 0