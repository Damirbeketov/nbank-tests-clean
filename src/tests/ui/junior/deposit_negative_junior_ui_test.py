from typing import List
import pytest, re
from playwright.sync_api import Page, Dialog, expect

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.tests.ui.base_test import BaseUITest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.skeleton.endpoint import Endpoint


@pytest.mark.ui

class TestDepositNegativeUI(BaseUITest):
    @pytest.mark.userfixtures("admin_user_request", "api_manager", "user_request")
    def test_user_can_create_account(self, page: Page, admin_user_request, api_manager,invalid_deposit_amount,user_request: CreateUserRequest):
        page.set_viewport_size({"width": 1920, "height": 1080})
        # ШАГ 1: админ залогинился в банке
        page.goto(f"{self.UI_BASE_URL}/login", wait_until="domcontentloaded")
        page.get_by_placeholder("Username").fill(admin_user_request.username)
        page.get_by_placeholder("Password").fill(admin_user_request.password)
        page.get_by_role("button").click()
        expect(page.get_by_text("Admin Panel")).to_be_visible()

        # ШАГ 2: админ создает юзера в банке
        new_user_request: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        page.get_by_placeholder("Username").fill(new_user_request.username)
        page.get_by_placeholder("Password").fill(new_user_request.password)

        # ШАГ 3: проверяем текст алерта
        def handle_create_user_dialog(dialog: Dialog):
            assert "User created successfully!" in dialog.message
            dialog.accept()

        page.once("dialog", handle_create_user_dialog)
        page.get_by_role("button", name="Add User").click()

        # ШАГ 4: проверяем, что пользователь есть на UI
        target = page.locator(
            f"xpath=//h2[text()='All Users']/following-sibling::li[contains(., '{new_user_request.username}')]"
        )
        expect(target).to_be_visible()

        # ШАГ 5: проверка, что юзер создан на API
        users = api_manager.admin_steps.get_all_users()
        created = [u for u in users if u.username == new_user_request.username]
        assert len(created) == 1
        ModelAssertions(created[0], new_user_request).match()

        # Авторизовываемся обычным пользователем
        page.goto(f"{self.UI_BASE_URL}/login", wait_until="domcontentloaded")
        page.get_by_placeholder("Username").fill(new_user_request.username)
        page.get_by_placeholder("Password").fill(new_user_request.password)
        page.get_by_role("button").click()

        # Первый вход — проверка что пользователь существует
        expect(page.get_by_text("User Dashboard")).to_be_visible()
        page.get_by_role("button", name="🚪 Logout").click()

        # Вход второй раз - для операций пользователя
        page.goto(f"{self.UI_BASE_URL}/login", wait_until="domcontentloaded")
        page.get_by_placeholder("Username").fill(new_user_request.username)
        page.get_by_placeholder("Password").fill(new_user_request.password)
        page.get_by_role("button", name="Login").click()

        expect(page.get_by_text("User Dashboard")).to_be_visible()

        # ШАГ 6: юзер создает аккаунт
        page.get_by_role("button", name="➕ Create New Account").click()

        # ШАГ 7: проверка, что аккаунт создался на UI
        def handle_create_account_dialog(dialog: Dialog):
            assert "✅ New Account Created! Account Number:" in dialog.message
            pattern = re.compile(r'Account Number: (\w+)')
            matcher = pattern.search(dialog.message)
            matcher.group(1)
            dialog.accept()

        page.once("dialog", handle_create_account_dialog)

        # ШАГ 8: проверка, что аккаунт был создан на API
        user_accounts: List[CreateAccountResponse] = ValidatedCrudRequester(
            RequestSpecs.auth_as_user(new_user_request.username, new_user_request.password),
            Endpoint.GET_CUSTOMER_ACCOUNTS,
            ResponseSpecs.request_returns_ok()
        ).get()

        assert len(user_accounts) == 1
        assert user_accounts[0] and user_accounts[0].balance == 0

        # ШАГ 9: Не валидный Deposit
        page.get_by_role("button", name=re.compile("Deposit Money")).click()
        page.select_option(".account-selector", value=user_accounts[0].accountNumber.replace("ACC", ""))
        page.get_by_placeholder("Enter amount").fill(str(invalid_deposit_amount))
        page.get_by_role("button", name=re.compile("Deposit")).click()

        # ШАГ 10: проверяем текст алерта
        def handle_create_deposit_dialog(dialog: Dialog):
            expected = f"Please deposit less or equal to 5000$."
            assert expected in dialog.message
            dialog.accept()

        page.once("dialog", handle_create_deposit_dialog)

        # ШАГ 11: проверяем Deposit через API
        transactions = api_manager.user_steps.get_account_transactions(
            new_user_request,
            user_accounts[0].id
        )

        assert len(transactions) == 0