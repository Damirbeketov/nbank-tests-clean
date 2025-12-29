import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert


@pytest.mark.ui
class TestTransferPositiveSeniorUI:
    @pytest.mark.user_session(1)
    def test_user_can_make_transfer(
        self,
        page: Page,
        api_manager: ApiManager,
        deposit_amount,
        transfer_amount,
    ):
        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        current_user = SessionStorage.get_user()

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(current_user)
        assert len(accounts) == 2

        from_account = accounts[0]
        to_account = accounts[1]

        # UI: депозит в from_account
        dashboard.open_deposit().deposit_money(str(from_account.id), deposit_amount)
        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_ACCOUNT)

        # API: проверка депозита
        txs_from = api_manager.user_steps.get_account_transactions(current_user, from_account.id)
        assert len(txs_from) >= 1
        last_tx = txs_from[0]
        assert float(last_tx.amount) == float(deposit_amount)
        assert last_tx.type == TransactionType.DEPOSIT

        # UI: трансфер
        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name="",
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount
        )
        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS)

        def has_transfer_in():
            txs_to = api_manager.user_steps.get_account_transactions(current_user, to_account.id)
            return txs_to if txs_to else None

        txs_to = None
        for _ in range(10):  # до ~2-3 секунд (зависит от скорости)
            txs_to = has_transfer_in()
            if txs_to:
                break
            page.wait_for_timeout(300)

        assert txs_to

        tx = txs_to[0]
        assert float(tx.amount) == float(transfer_amount)
        assert tx.type == TransactionType.TRANSFER_IN
        assert tx.relatedAccountId == from_account.id