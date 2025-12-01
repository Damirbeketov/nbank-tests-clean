import requests
from src.main.api.requests.requester import Requester
from src.main.api.models.transaction_response import TransactionResponse


class GetAccountTransactionsRequester(Requester):
    def __init__(self, spec, response_spec):
        super().__init__(spec, response_spec)

    def get(self, account_id: int):
        url = f"{self.base_url}/accounts/{account_id}/transactions"

        response = requests.get(
            url=url,
            headers=self.headers
        )

        self.response_spec(response)

        json_list = response.json()

        if not json_list:
            return []
        return [TransactionResponse(**item) for item in json_list]

    def post(self, *args, **kwargs):
        pass