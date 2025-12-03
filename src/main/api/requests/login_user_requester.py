import requests
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.requests.requester import Requester



class LoginUserRequester(Requester):
    def post(self, login_user_request: LoginUserRequest) -> LoginUserResponse:
        url = f'{self.base_url}/auth/login'
        response= requests.post(url=url, json=login_user_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        return LoginUserResponse(**response.json())




