from src.main.ui.pages.base_page import BasePage

class DepositPage(BasePage):
    @property
    def welcome_text(self):
        return self.page.get_by_text("💰 Deposit Money")

    @property
    def account_selector(self):
        return self.page.locator(".account-selector")

    def url(self):
        return "/deposit"

    @property
    def amount_input(self):
        return self.page.get_by_placeholder("Enter amount")

    @property
    def deposit_button(self):
        return self.page.get_by_role("button", name="Deposit")

    def deposit_money(self, account_id: str, amount: float):
        self.account_selector.select_option(account_id)
        self.amount_input.fill(str(amount))
        self.deposit_button.click()
        return self

    def deposit_money_as_user(self, amount: float):
        self.amount_input.fill(str(amount))
        self.deposit_button.click()
        return self


