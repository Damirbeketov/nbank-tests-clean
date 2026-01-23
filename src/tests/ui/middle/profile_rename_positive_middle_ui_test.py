import pytest
from playwright.sync_api import Page, expect

from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard
from src.tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestProfileRenamePositiveUI(BaseUITest):

    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_profile_rename_positive(
        self,
        page: Page,
        api_manager,
        deposit_amount,
        transfer_amount,
        new_user_name,
        user_request,
    ):
        # ШАГ 1: логин
        self.auth_as_user(page, user_request)

        dashboard = UserDashboard(page).open()
        expect(dashboard.welcome_text).to_be_visible()

        # проверяем что у нового пользователя дефолтное имя
        expect(dashboard.user_name).to_have_text("noname")

        # меняем имя
        edit_profile = dashboard.open_edit_profile()
        with page.expect_event("dialog") as dialog_info:
            edit_profile.edit_profile(new_user_name)

        dialog = dialog_info.value
        assert BankAlert.EDIT_PROFILE_SUCCESS in dialog.message
        dialog.accept()

        # возвращаемся домой и проверяем имя
        page.get_by_role("button", name="Home").click()
        dashboard = UserDashboard(page)
        expect(dashboard.user_name).to_have_text(new_user_name)

        # создаем два аккаунта
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(user_request)
        assert len(accounts) == 2
        from_account = accounts[0]
        to_account = accounts[1]

        # депозит
        dashboard.open_deposit().deposit_money(str(from_account.id), deposit_amount)
        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_ACCOUNT)

        txs_from = api_manager.user_steps.get_account_transactions(user_request, from_account.id)
        assert len(txs_from) == 1
        assert txs_from[0].amount == deposit_amount
        assert txs_from[0].type == TransactionType.DEPOSIT

        # трансфер (recipient_name = новое имя)
        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name=new_user_name,
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount,
        )
        dashboard.check_alert_message_and_accept(BankAlert.TRANSFER_SUCCESS)

        # вместо sleep: ждём появления TRANSFER_IN
        def has_transfer_in():
            txs = api_manager.user_steps.get_account_transactions(user_request, to_account.id)
            return [t for t in txs if t.type == TransactionType.TRANSFER_IN and t.amount == transfer_amount]

        txs_to = None
        for _ in range(10):
            txs_to = has_transfer_in()
            if txs_to:
                break
            page.wait_for_timeout(300)

        assert txs_to, "TRANSFER_IN не появился в истории транзакций"

        tx = txs_to[-1]
        assert tx.amount == transfer_amount
        assert tx.type == TransactionType.TRANSFER_IN
        assert tx.relatedAccountId == from_account.id