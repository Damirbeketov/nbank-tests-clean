import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.profile_request import ProfileRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.profile_requester import ProfileRequester
from src.main.api.requests.steps.get_profile_requester import GetProfileRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestProfileRenameMiddle:

    @pytest.mark.parametrize(
        "name",
        ["New Name", "new name", "Name new", "name New", "NEW NAME", "N N", "n n"]
    )
    def test_profile_rename_positive(self, name):
        username = RandomData.get_username()
        password = RandomData.get_password()
        user = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user)

        rename_response = ProfileRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).put(ProfileRequest(name=name))

        assert rename_response.customer.name == name
        assert rename_response.message == "Profile updated successfully"

        profile = GetProfileRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get()

        assert profile.name == name