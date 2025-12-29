import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert


@pytest.mark.ui
class TestDepositNegativeUI:
    @pytest.mark.user_session(1)
    def test_user_cannot_make_negative_deposit(
        self,
        page: Page,
        api_manager: ApiManager,
        invalid_deposit_amount,
    ):

        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        current_user = SessionStorage.get_user()

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)


        accounts = api_manager.user_steps.get_all_accounts(current_user)
        assert len(accounts) == 1
        account = accounts[0]

        dashboard.open_deposit().deposit_money(str(account.id), invalid_deposit_amount)

        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_NEGATIVE_ACCOUNT)

        transactions = api_manager.user_steps.get_account_transactions(current_user, account.id)
        assert len(transactions) == 0