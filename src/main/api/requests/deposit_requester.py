from http import HTTPStatus
import requests
from src.main.api.requests.requester import Requester
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse


class DepositRequester(Requester):
    def post(self, deposit_request: DepositRequest):
        url = f"{self.base_url}/accounts/deposit"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=deposit_request.model_dump()
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return DepositResponse(**response.json())

        return response