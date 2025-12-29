import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard


@pytest.mark.ui
@pytest.mark.xfail(reason="BUG: Transfer Again (TRANSFER_OUT) uses same account as source and target")
class TestTransferInAgainSeniorUI:

    @pytest.mark.user_session(1)
    def test_transfer_in(
        self,
        page: Page,
        api_manager: ApiManager,
        deposit_amount,
        transfer_amount,
    ):
        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()


        current_user = SessionStorage.get_user()

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

        #проверка депозита через API
        transactions = api_manager.user_steps.get_account_transactions(current_user, from_account.id)

        assert len(transactions) == 1
        assert transactions[0].amount == deposit_amount
        assert transactions[0].type == TransactionType.DEPOSIT

        # Делаем Трансфер
        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name="",
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount,
        )

        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS)

        transactions = api_manager.user_steps.get_account_transactions(current_user, to_account.id)

        tx = transactions[0]
        assert tx.amount == transfer_amount
        assert tx.type == TransactionType.TRANSFER_IN
        assert tx.relatedAccountId == from_account.id

        # переходим во вкладку TransferAgain
        transfer_page = dashboard.open_transfer()
        transfer_page.repeat_transfer_in_flow(from_account)

        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS_OUT)

        # проверки через API (как у тебя)
        transactions = api_manager.user_steps.get_account_transactions(current_user, to_account.id)

        tx = transactions[-1]
        assert tx.amount == transfer_amount
        assert tx.type == TransactionType.TRANSFER_IN
        assert tx.relatedAccountId == from_account.id