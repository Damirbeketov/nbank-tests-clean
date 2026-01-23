import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert


@pytest.mark.ui
class TestTransferNegativeSeniorUI:

    @pytest.mark.user_session(1)
    def test_transfer_negative(
        self,
        page: Page,
        api_manager: ApiManager,
        deposit_amount,
        invalid_amount,
    ):

        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        # ✅ тот же пользователь для API
        current_user = SessionStorage.get_user()  # если нужно: get_user(0)

        #создаем два аккаунта
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(current_user)
        assert len(accounts) == 2
        from_account = accounts[0]
        to_account = accounts[1]

        #депозит
        dashboard.open_deposit().deposit_money(str(from_account.id), deposit_amount)
        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_ACCOUNT)

        # проверка депозита через API
        transactions = api_manager.user_steps.get_account_transactions(current_user, from_account.id)
        assert len(transactions) == 1
        assert float(transactions[0].amount) == float(deposit_amount)
        assert transactions[0].type == TransactionType.DEPOSIT

        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name="",
            recipient_account_number=to_account.accountNumber,
            amount=invalid_amount,
        )


        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_INVALID)


        transactions = api_manager.user_steps.get_account_transactions(current_user, to_account.id)
        assert len(transactions) == 0