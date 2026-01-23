from playwright.sync_api import Page

from src.main.api.configs.config import Config
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.models.create_user_request import CreateUserRequest


class BaseUITest:
    UI_BASE_URL = Config.get("UI_BASE_URL", "http://localhost:3000")

    def auth_as_user(self, page: Page, user_request: CreateUserRequest) -> None:
        spec = RequestSpecs.auth_as_user(user_request.username, user_request.password)

        headers = spec.get("headers")
        assert isinstance(headers, dict), f"RequestSpecs.auth_as_user must return dict with 'headers'. spec={spec}"

        auth_token = headers.get("Authorization") or headers.get("authorization")
        assert auth_token, f"Authorization header missing. headers={headers}"

        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(self.UI_BASE_URL)
        page.evaluate('token => localStorage.setItem("authToken", token)', auth_token)

        # чтобы UI точно подхватил токен
        assert page.evaluate('() => localStorage.getItem("authToken")'), "authToken not set"
        page.reload()