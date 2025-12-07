from cProfile import Profile

from src.main.api.models.get_account_transaction_response import GetAccountTransactionResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.profile_request import ProfileRequest
from src.main.api.models.profile_response import ProfileResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class UserSteps(BaseSteps):
    def login(self, user_request: CreateUserRequest) -> LoginUserResponse:
        login_request = LoginUserRequest(username=user_request.username, password=user_request.password)
        login_response: LoginUserResponse = ValidatedCrudRequester(
            RequestSpecs.unauth_spec(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_returns_ok()
        ).post(login_request)
        ModelAssertions(login_request, login_response).match()
        return login_response

    def create_account(self, user_request: CreateUserRequest) -> CreateAccountResponse:
        create_account_response: CreateAccountResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.entity_was_created()
        ).post()

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions
        return create_account_response

    def deposit_account(self, user_request, account_id, amount) -> DepositResponse:
        deposit_response: DepositResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_returns_ok()
        ).post(DepositRequest(id=account_id, balance=amount))
        return deposit_response

    def transfer_account(self, user_request, sender_account_id, receiver_account_id, amount) -> TransferResponse:
        transfer_response: TransferResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_returns_ok()
        ).post(TransferRequest(senderAccountId=sender_account_id, receiverAccountId=receiver_account_id,amount=amount))
        return transfer_response

    def profile_rename(self, user_request: CreateUserRequest, name) -> ProfileResponse:
        profile_response: ProfileResponse = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.RENAME_ACCOUNT,
            ResponseSpecs.request_returns_ok()
        ).put(ProfileRequest(name=name))
        return profile_response