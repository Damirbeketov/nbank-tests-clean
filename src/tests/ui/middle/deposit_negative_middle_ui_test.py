from typing import List
import pytest, re
from playwright.sync_api import Page, Dialog, expect

from src.main.api.models.transaction_type import TransactionType
from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.user_dashboard import UserDashboard
from src.tests.ui.base_test import BaseUITest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.ui
class TestDepositPositiveUI(BaseUITest):

    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_deposit_positive(
        self,
        page: Page,
        api_manager,
        invalid_deposit_amount,
        user_request: CreateUserRequest
    ):
        # ШАГ 1: логин
        self.auth_as_user(page, user_request)

        # ШАГ 2: создать аккаунт
        dashboard = UserDashboard(page).open()
        dashboard.create_new_account()
        dashboard.check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        accounts = api_manager.user_steps.get_all_accounts(user_request)
        account = accounts[0]

        # ШАГ 3: депозит
        dashboard.open_deposit().deposit_money(
            str(account.id),
            invalid_deposit_amount
        )
        # Проверяем аллерт
        dashboard.check_alert_message_and_accept(
            BankAlert.DEPOSIT_MONEY_NEGATIVE_ACCOUNT
        )

        # ШАГ 4: проверка через API
        transactions = api_manager.user_steps.get_account_transactions(
            user_request,
            account.id
        )

        assert len(transactions) == 0