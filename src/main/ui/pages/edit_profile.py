from src.main.ui.pages.base_page import BasePage

class EditProfile(BasePage):
    @property
    def welcome_text_profile(self):
        return self.page.get_by_role("heading", name="✏️ Edit Profile")

    def url(self):
        return "/edit-profile"

    @property
    def enter_new_name(self):
        return self.page.get_by_placeholder("Enter new name")

    @property
    def save_changes_button(self):
        return self.page.get_by_role("button", name="Save Changes")


    def edit_profile(self,new_name:str):
        self.enter_new_name.fill(new_name)
        self.save_changes_button.click()
        return self






