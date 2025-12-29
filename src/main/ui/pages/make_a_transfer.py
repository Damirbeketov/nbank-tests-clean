from src.main.ui.pages.base_page import BasePage

class TransferPage(BasePage):
    @property
    def welkome_text(self):
        return self.page.get_by_text("🔄 Make a Transfer")

    @property
    def url(self):
        return "/transfer"

    @property
    def select_your_account(self):
        return self.page.locator(".account-selector")

    @property
    def recipient_name(self):
        return self.page.get_by_placeholder("Enter recipient name")

    @property
    def recipient_account_number(self):
        return self.page.get_by_placeholder("Enter recipient account number")

    @property
    def amount(self):
        return self.page.get_by_placeholder("Enter amount")

    @property
    def confirm_check(self):
        return self.page.locator("#confirmCheck")

    @property
    def send_transfer_button(self):
        return self.page.get_by_role("button", name="Send Transfer")

    def make_a_transfer(self,from_account_id: str,recipient_name: str,recipient_account_number: str,amount: float):
        self.select_your_account.select_option(from_account_id)
        self.recipient_name.fill(recipient_name)
        self.recipient_account_number.fill(recipient_account_number)
        self.amount.fill(str(amount))
        self.confirm_check.check()
        self.send_transfer_button.click()
        return self

    def make_a_transfer_without_confirm(self,from_account_id: str,recipient_name: str,recipient_account_number: str,amount: float):
        self.select_your_account.select_option(from_account_id)
        self.recipient_name.fill(recipient_name)
        self.recipient_account_number.fill(recipient_account_number)
        self.amount.fill(str(amount))
        self.send_transfer_button.click()
        return self

    @property
    def transfer_again(self):
        return self.page.get_by_role("button", name="Transfer Again")

    @property
    def transfer_out(self):
        return self.page.get_by_role("button", name="Repeat")

    @property
    def account_selector(self):
        return self.page.locator("select.form-control")

    @property
    def confirm_check(self):
        return self.page.locator("#confirmCheck")

    @property
    def send_transfer_button(self):
        return self.page.get_by_role("button", name="Send Transfer")

    def open_transfer_again(self):
        self.page.reload()
        self.transfer_again_button.click()
        return self

    def repeat_transfer_out(self):
        self.page.locator("li",has_text="TRANSFER_OUT").get_by_role("button",name="Repeat").click()
        return self

    def select_source_account(self, account_id: str):
        self.account_selector.select_option(account_id)
        return self

    def confirm_and_send(self):
        self.confirm_check.check()
        self.send_transfer_button.click()
        return self

    def repeat_transfer_out_flow(self, source_account_id: str):
        self.open_transfer_again()
        self.repeat_transfer_out()
        self.select_source_account(source_account_id)
        self.confirm_and_send()
        return self

    def repeat_transfer_in(self):
        self.page.locator("li",has_text="TRANSFER_IN").get_by_role("button",name="Repeat").click()
        return self

    def repeat_transfer_in_flow(self, source_account_id: str):
        self.open_transfer_again()
        self.repeat_transfer_in()
        self.select_source_account(source_account_id)
        self.confirm_and_send()
        return self



