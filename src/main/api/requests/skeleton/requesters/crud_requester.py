from typing import Optional, TypeVar
import requests
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface

T = TypeVar('T', bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):

    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ""

        response = requests.post(
            url=f"{self.base_url}{self.endpoint.value.url}",
            headers=self.headers,
            json=body
        )
        self.response_spec(response)
        return response

    def get(self, id: int = None) -> requests.Response:
        if id is not None:
            url = f"{self.base_url}{self.endpoint.value.url}/{id}"
        else:
            url = f"{self.base_url}{self.endpoint.value.url}"

        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        return response


    def get_path(self, **path_params) -> requests.Response:
        url = self.endpoint.value.url.format(**path_params)

        response = requests.get(
            url=f"{self.base_url}{url}",
            headers=self.headers
        )
        self.response_spec(response)
        return response

    def delete(self, id: int) -> requests.Response:
        response = requests.delete(
            url=f"{self.base_url}{self.endpoint.value.url}/{id}",
            headers=self.headers
        )
        self.response_spec(response)
        return response

    def put(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model is not None else ""

        response = requests.put(
            url=f"{self.base_url}{self.endpoint.value.url}",
            headers=self.headers,
            json=body
        )
        self.response_spec(response)
        return response