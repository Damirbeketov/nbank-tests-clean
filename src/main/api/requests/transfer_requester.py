from http import HTTPStatus
import requests
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest) -> TransferResponse:
        url=f'{self.base_url}/accounts/transfer'
        response=requests.post(url=url, headers=self.headers, json=transfer_request.model_dump())
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return TransferResponse(**response.json())

