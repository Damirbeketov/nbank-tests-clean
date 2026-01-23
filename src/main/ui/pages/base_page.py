from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Callable, List
from playwright.sync_api import Page, Dialog, Locator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.configs.config import Config

T = TypeVar("T", bound="BasePage")


class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.base_url = str(Config.get("UI_BASE_URL", "http://localhost:3000")).rstrip("/")

    @property
    def username_input(self):
        return self.page.get_by_placeholder("Username")

    @property
    def password_input(self):
        return self.page.get_by_placeholder("Password")

    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    def open(self: T) -> T:
        target = self.url()
        if self.base_url and target.startswith("/"):
            target = f"{self.base_url}{target}"
        self.page.goto(target, wait_until="domcontentloaded")
        return self

    def get_page(self, page_cls: Type[T]) -> T:
        return page_cls(self.page)

    def check_alert_message_and_accept(self: T, expected_text: str) -> T:
        def _handler(d: Dialog) -> None:
            assert expected_text in d.message, f"Alert text mismatch: {d.message!r}"
            d.accept()

        self.page.once("dialog", _handler)
        return self

    def auth_as_user(self, user_request):
        spec = RequestSpecs.auth_as_user(user_request.username, user_request.password)

        headers = spec.get("headers")
        assert isinstance(headers, dict), f"RequestSpecs.auth_as_user must return dict with 'headers'. spec={spec}"

        auth_token = headers.get("Authorization") or headers.get("authorization")
        assert auth_token, f"Authorization header missing. headers={headers}"

        self.page.goto(self.base_url)
        self.page.evaluate("token => localStorage.setItem('authToken', token)", auth_token)
        assert self.page.evaluate("() => localStorage.getItem('authToken')"), "authToken not set"
        self.page.reload()

    def _generate_page_elements(self, elements: Locator, constructor: Callable[[Locator], T]) -> List[T]:
        elements.first.wait_for(state="attached", timeout=10_000)
        return [constructor(elements.nth(i)) for i in range(elements.count())]

    def expect_alert_and_accept(
            self,
            expected_text: str,
            action: Callable[[], None],
    ):
        with self.page.expect_event("dialog") as dialog_info:
            action()

        dialog = dialog_info.value
        assert expected_text in dialog.message, (
            f"Alert text mismatch: {dialog.message!r}"
        )
        dialog.accept()
        return self