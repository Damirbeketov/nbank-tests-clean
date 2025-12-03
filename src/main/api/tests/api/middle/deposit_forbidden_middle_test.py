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
class TestDepositForbiddenMiddle:

    @pytest.mark.parametrize(
        "balance, expected_error",
        [
            (1000, "Unauthorized access to account"),
        ]
    )
    def test_deposit_forbidden(self, balance, expected_error):
        # создаём user 1
        username1 = RandomData.get_username()
        password1 = RandomData.get_password()
        user1 = CreateUserRequest(username=username1, password=password1, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user1)

        # создаём user 2
        username2 = RandomData.get_username()
        password2 = RandomData.get_password()
        user2 = CreateUserRequest(username=username2, password=password2, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user2)

        # создаём аккаунт для user1
        account_1 = CreateAccountRequester(
            RequestSpecs.auth_as_user(username1, password1),
            ResponseSpecs.entity_was_created()
        ).post()

        # создаём аккаунт для user2
        CreateAccountRequester(
            RequestSpecs.auth_as_user(username2, password2),
            ResponseSpecs.entity_was_created()
        ).post()

        # user2 пытается пополнить account_1
        response = DepositRequester(
            RequestSpecs.auth_as_user(username2, password2),
            ResponseSpecs.forbidden()
        ).post(DepositRequest(id=account_1.id, balance=balance))

        # проверяем текст ошибки
        assert expected_error in response.text

        # проверяем отсутствие транзакций
        transactions = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(username1, password1),
            ResponseSpecs.request_returns_ok()
        ).get(account_1.id)

        assert len(transactions) == 0

    def test_deposit_account_not_found(self):
        # создаём одного юзера
        username = RandomData.get_username()
        password = RandomData.get_password()
        user = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user)

        nonexistent_id = 999999999

        # user пытается пополнить несуществующий аккаунт
        response = DepositRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.forbidden()
        ).post(DepositRequest(id=nonexistent_id, balance=1000))

        assert "Unauthorized access to account" in response.text