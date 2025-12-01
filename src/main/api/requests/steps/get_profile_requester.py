import requests
from src.main.api.models.profile_get_response import ProfileGetResponse
from src.main.api.requests.requester import Requester


class GetProfileRequester(Requester):
    def get(self):
        url = f"{self.base_url}/customer/profile"
        response = requests.get(url=url, headers=self.headers)

        self.response_spec(response)
        return ProfileGetResponse(**response.json())

    def post(self, *args, **kwargs):
        pass