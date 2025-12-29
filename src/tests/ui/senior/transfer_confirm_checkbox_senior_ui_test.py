import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard


@pytest.mark.ui
class TestTransferConfirmRequiredSeniorUI:

    @pytest.mark.user_session(1)
    def test_transfer_without_confirm_does_not_create_transaction(
        self,
        page: Page,
        api_manager: ApiManager,
        deposit_amount,
        transfer_amount,
    ):
        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()


        current_user = SessionStorage.get_user()  # если нужно: get_user(0)

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(current_user)
        assert len(accounts) == 2
        from_account = accounts[0]
        to_account = accounts[1]

        dashboard.open_deposit().deposit_money(str(from_account.id), deposit_amount)
        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_ACCOUNT)

        transactions = api_manager.user_steps.get_account_transactions(current_user, from_account.id)
        assert len(transactions) == 1
        assert float(transactions[0].amount) == float(deposit_amount)
        assert transactions[0].type == TransactionType.DEPOSIT

        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer_without_confirm(
            from_account_id=str(from_account.id),
            recipient_name="",
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount,
        )

        dashboard.check_alert_message_and_accept(BankAlert.CONFIRM_CHECK)

        transactions = api_manager.user_steps.get_account_transactions(current_user, to_account.id)
        assert len(transactions) == 0