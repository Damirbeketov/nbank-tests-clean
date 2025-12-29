import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.api
class TestProfileRename:
    @pytest.mark.parametrize(
        "name",
        ["New Name", "new name", "Name new", "name New", "NEW NAME", "N N", "n n"]
    )
    @pytest.mark.usefixtures('user_request', 'api_manager')
    def test_rename(self, api_manager: ApiManager, user_request: CreateUserRequest, name):
        api_manager.user_steps.login(user_request)
        new_name = api_manager.user_steps.profile_rename(user_request, name)

        assert new_name.customer.name == name
        assert new_name.message == "Profile updated successfully"

        # проверка изменения имени
        rename = api_manager.user_steps.get_customer_profile(user_request)
        assert rename.name == name


