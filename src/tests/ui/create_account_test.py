import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert

@pytest.mark.ui
class TestCreateAccount:
    @pytest.mark.user_session(10)
    def test_user_can_create_account(self, api_manager: ApiManager, page: Page, current_user):
        dashboard_page = UserDashboard(page).open()
        expect(dashboard_page.welcome_text).to_be_visible()

        dashboard_page = dashboard_page.create_new_account()
        dashboard_page.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        # ВАЖНО: проверяем аккаунты того же юзера, который залогинен в UI
        user_accounts = api_manager.user_steps.get_all_accounts(current_user)

        assert len(user_accounts) == 1
        assert user_accounts[0].balance == 0