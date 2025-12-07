from src.main.api.requests.requester import Requester
from src.main.api.models.create_account_response import CreateAccountResponse
import requests

class CreateAccountRequester(Requester):
    def post(self):
        url = f"{self.base_url}/accounts"
        response = requests.post(url, headers=self.headers)
        self.response_spec(response)
        return CreateAccountResponse(**response.json())