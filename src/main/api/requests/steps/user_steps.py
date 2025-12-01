import requests

from src.main.api.models.get_account_transaction_response import GetAccountTransactionResponse
from src.main.api.configs.config import Config
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.profile_request import ProfileRequest
from src.main.api.models.profile_response import ProfileResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.requests.skeleton.requesters.get_account_transactions_requester import GetAccountTransactionsRequester
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.steps.base_steps import BaseSteps
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest



class UserSteps(BaseSteps):
    def create_account(self, user_request: CreateUserRequest):
        return ValidatedCrudRequester(
            RequestSpecs.auth_as_user(
                user_request.username,
                user_request.password
            ),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.entity_was_created()
        ).post(None)

    def login(self, user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.unauth_spec(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_returns_ok()
        ).post(LoginUserRequest(
            username=user_request.username,
            password=user_request.password
        ))
        assert response.headers.get('Authorization')
        return response

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

    def profile_rename_negative(self, user_request, name, expected_message):
        return CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.RENAME_ACCOUNT,
            ResponseSpecs.bad_request_with_text(expected_message)
        ).put(ProfileRequest(name=name))

    def get_account_transactions(self, user_request, account_id: int) -> list[GetAccountTransactionResponse]:
        response_json = GetAccountTransactionsRequester(
            RequestSpecs.auth_as_user(
                user_request.username,
                user_request.password
            ),
            Endpoint.TRANSACTION_ACCOUNT,
            ResponseSpecs.request_returns_ok()
        ).get(account_id)

        if isinstance(response_json, dict):
            data = response_json.get("transactions", [])
        else:
            data = response_json

        return [GetAccountTransactionResponse(**item) for item in data]

    def get_account_transactions_raw(self, user_request, account_id):
        url = Endpoint.TRANSACTION_ACCOUNT.value.url.replace("{account_id}", str(account_id))

        response = requests.get(
            url=f"{Config.get('server')}{Config.get('api_version')}{url}",
            headers=RequestSpecs.auth_as_user(
                user_request.username,
                user_request.password
            )
        )
        return response

    def deposit_account_forbidden(self, user_request, account_id, amount):
        return CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.forbidden(),
        ).post(DepositRequest(id=account_id, balance=amount))

    def transfer_account_negative(self, user_request, sender_account_id, receiver_account_id, amount, expected_message):
        return CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.bad_request_with_text(expected_message)
        ).post(
            TransferRequest(
                senderAccountId=sender_account_id,
                receiverAccountId=receiver_account_id,
                amount=amount
            )
        )

    def get_customer_profile(self, user_request):
        return ValidatedCrudRequester(
            RequestSpecs.auth_as_user(
                user_request.username,
                user_request.password
            ),
            Endpoint.GET_PROFILE,
            ResponseSpecs.request_returns_ok()
        ).get()

    def deposit_account_negative(self, user_request, account_id, amount, expected_message):
        return CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.bad_request_with_text(expected_message)
        ).post(
            DepositRequest(
                id=account_id,
                balance=amount
            )
        )










