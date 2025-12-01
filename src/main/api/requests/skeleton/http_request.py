from typing import Protocol, Dict, Callable

from src.main.api.requests.skeleton.endpoint import Endpoint


class HttpRequest:
    def __init__(self, request_spec, endpoint, response_spec):
        self.request_spec = request_spec
        self.headers = request_spec["headers"]
        self.base_url = request_spec["base_url"]
        self.endpoint = endpoint
        self.response_spec = response_spec