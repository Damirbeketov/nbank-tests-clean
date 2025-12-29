from src.main.ui.pages.bank_alert import BankAlert
from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.deposit_page import DepositPage
from src.main.ui.pages.edit_profile import EditProfile
from src.main.ui.pages.make_a_transfer import TransferPage


class UserDashboard(BasePage):
    @property
    def welcome_text(self):
        return self.page.get_by_text("User Dashboard")

    @property
    def create_new_account_button(self):
        return self.page.get_by_role("button", name="➕ Create New Account")

    def url(self):
        return "/dashboard"

    def create_new_account(self):
        self.create_new_account_button.click()
        return self

    @property
    def deposit_button(self):
        return self.page.get_by_role("button", name="Deposit Money")

    @property
    def make_a_transfer_button(self):
        return self.page.get_by_role("button", name="Make A Transfer")

    def open_deposit(self) -> DepositPage:
        self.deposit_button.click()
        return DepositPage(self.page)

    def open_transfer(self) -> TransferPage:
        self.make_a_transfer_button.click()
        return TransferPage(self.page)

    @property
    def user_name(self):
        return self.page.locator("h2.welcome-text span")

    def open_edit_profile(self) -> EditProfile:
        self.page.locator("div.profile-header").click()
        return EditProfile(self.page)

    def create_new_account_and_expect_alert(self, expected_text: str):
        with self.page.expect_event("dialog") as d:
            self.create_new_account_button.click(no_wait_after=True)

        dialog = d.value
        assert expected_text in dialog.message, f"Alert text mismatch: {dialog.message!r}"
        dialog.accept()
        return self
