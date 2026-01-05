import pytest
from playwright.sync_api import Page, expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard


@pytest.mark.ui
class TestProfileRenamePositiveSeniorUI:

    @pytest.mark.user_session(1)
    def test_profile_rename_positive(
        self,
        page: Page,
        api_manager: ApiManager,
        deposit_amount: float,
        transfer_amount: float,
        new_user_name: str,
    ):
        current_user = SessionStorage.get_user()

        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        expect(dashboard.user_name).to_have_text("noname")

        edit_profile = dashboard.open_edit_profile()
        with page.expect_event("dialog") as dialog_info:
            edit_profile.edit_profile(new_user_name)

        dialog = dialog_info.value
        assert BankAlert.EDIT_PROFILE_SUCCESS in dialog.message
        dialog.accept()

        page.get_by_role("button", name="Home").click()
        dashboard = UserDashboard(page)
        expect(dashboard.user_name).to_have_text(new_user_name)

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

        txs_from = api_manager.user_steps.get_account_transactions(current_user, from_account.id)
        assert len(txs_from) == 1
        assert txs_from[0].amount == deposit_amount
        assert txs_from[0].type == TransactionType.DEPOSIT

        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name=new_user_name,
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount,
        )
        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS)

        txs_to = api_manager.user_steps.wait_transfer_in_with_retry(
            current_user,
            to_account.id,
            transfer_amount,
            page=page,
        )

        tx = txs_to[-1]
        assert tx.relatedAccountId == from_account.id