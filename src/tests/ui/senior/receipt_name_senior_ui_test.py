import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard


@pytest.mark.ui
class TestReceiptNameSeniorUI:
    @pytest.mark.parametrize(
        "recipient_name",
        [
            "transfer",
            "Transfer Transfer",
            "transfer transfer transfer",
            "перевод123",
            "TRANSFER",
            "12345",
            "перевод!",
            "transfer?",
            "transfer146",
            " ",
            "  ",
            "🚀",
            "a" * 255,
        ],
    )
    @pytest.mark.user_session(1)
    def test_receipt_name(
        self,
        page: Page,
        api_manager: ApiManager,
        recipient_name: str,
        deposit_amount: float,
        transfer_amount: float,
    ):
        # UI: юзер уже залогинен фикстурой user_session_extension
        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        current_user = SessionStorage.get_user()

        # 1) Создаём 2 аккаунта через UI
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


        tx_from = api_manager.user_steps.get_account_transactions(current_user, from_account.id)
        assert len(tx_from) == 1
        assert tx_from[0].amount == deposit_amount
        assert tx_from[0].type == TransactionType.DEPOSIT

        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name=recipient_name,
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount,
        )
        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS)

        tx_in = None
        for _ in range(10):  # ~3 секунды
            txs_to = api_manager.user_steps.get_account_transactions(current_user, to_account.id)
            transfer_ins = [t for t in txs_to if t.type == TransactionType.TRANSFER_IN]
            if transfer_ins:
                tx_in = transfer_ins[-1]
                break
            page.wait_for_timeout(300)

        assert tx_in is not None, "TRANSFER_IN not found on recipient account"
        assert tx_in.amount == transfer_amount
        assert tx_in.type == TransactionType.TRANSFER_IN
        assert tx_in.relatedAccountId == from_account.id