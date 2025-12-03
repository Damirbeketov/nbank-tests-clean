import requests
from src.main.api.requests.skeleton.http_request import HttpRequest

class GetAccountTransactionsRequester(HttpRequest):
    def get(self, account_id: int):
        url = self.endpoint.value.url.replace("{account_id}", str(account_id))
        response = requests.get(
            url=f"{self.base_url}{url}",
            headers=self.headers
        )

        self.response_spec(response)
        return response.json()