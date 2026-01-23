from typing import List
import pytest, re
from playwright.sync_api import Page, Dialog, expect
import time

from src.main.api.fixtures.user_fixtures import new_user_name
from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard
from src.tests.ui.base_test import BaseUITest
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.ui

class TestProfileRenameNegativeUI(BaseUITest):
    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_profile_rename_negative(self, page: Page, api_manager, deposit_amount, transfer_amount, new_user_name, user_request: CreateUserRequest):
        # ШАГ 1: логин
        self.auth_as_user(page, user_request)

        # ШАГ 2: создаем два аккаунта
        dashboard = UserDashboard(page).open()
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(user_request)
        assert len(accounts) == 2
        from_account = accounts[0]
        to_account = accounts[1]

        # проверяем что у нового пользователя нет имени
        dashboard = UserDashboard(page).open()
        expect(dashboard.user_name).to_have_text("noname")

        # создаем имя пользователю
        dashboard = UserDashboard(page).open()
        edit_profile = dashboard.open_edit_profile()

        with page.expect_event("dialog") as dialog_info:
            edit_profile.edit_profile(new_user_name)

        dialog = dialog_info.value
        assert BankAlert.EDIT_PROFILE_SUCCESS in dialog.message
        dialog.accept()

        page.get_by_role("button", name="Home").click()
        dashboard = UserDashboard(page)

        expect(dashboard.user_name).to_have_text(new_user_name)

        # ШАГ 3: депозит
        dashboard.open_deposit().deposit_money(str(from_account.id),deposit_amount)

        # Проверяем аллерт
        dashboard.check_alert_message_and_accept(BankAlert.DEPOSIT_MONEY_ACCOUNT)

        # ШАГ 4: проверка через API
        transactions = api_manager.user_steps.get_account_transactions(user_request,from_account.id)

        assert len(transactions) == 1
        assert transactions[0].amount == deposit_amount
        assert transactions[0].type == TransactionType.DEPOSIT

        # ШАГ 12: Делаем Трансфер
        transfer_page = dashboard.open_transfer()
        transfer_page.make_a_transfer(
            from_account_id=str(from_account.id),
            recipient_name="",
            recipient_account_number=to_account.accountNumber,
            amount=transfer_amount
        )

        # проверяем аллерт трансфера
        dashboard.check_alert_message_and_accept(
            BankAlert.NAME_NOT_MATCH
        )
        # проверки через API
        time.sleep(1)  # даём бэкенду время сохранить трансфер

        transactions = api_manager.user_steps.get_account_transactions(
            user_request,
            to_account.id
        )

        assert len(transactions) == 0


