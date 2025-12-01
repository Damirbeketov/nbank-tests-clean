import requests
from src.main.api.requests.requester import Requester
from src.main.api.models.profile_request import ProfileRequest
from src.main.api.models.profile_response import ProfileResponse


class ProfileRequester(Requester):

    def put(self, body: ProfileRequest):
        url = f"{self.base_url}/customer/profile"
        response = requests.put(url=url, json=body.model_dump(), headers=self.headers)
        self.response_spec(response)

        if response.status_code == 200:
            return ProfileResponse(**response.json())
        return response.text

    def get(self):
        url = f"{self.base_url}/customer/profile"
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return ProfileResponse(**response.json())

    def post(self, *args, **kwargs):
        pass