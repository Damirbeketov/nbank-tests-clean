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
class TestProfileRenameNegativeMiddle:

    @pytest.mark.parametrize(
        "name, expected_message",
        [
            ('UserName', 'Name must contain two words with letters only'),
            ('User! Name', 'Name must contain two words with letters only'),
            ('User Name1', 'Name must contain two words with letters only'),
            ('user name.', 'Name must contain two words with letters only'),
            (' User Name', 'Name must contain two words with letters only'),
        ]
    )
    def test_profile_rename_negative(self, name, expected_message):

        username = RandomData.get_username()
        password = RandomData.get_password()
        user = CreateUserRequest(username=username, password=password, role="USER")

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user)

        old_profile = GetProfileRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get()

        old_name = old_profile.name

        # отправляем невалидное имя
        ProfileRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.bad_request_text(expected_message)
        ).put(ProfileRequest(name=name))

        # проверяем что имя не изменилось
        new_profile = GetProfileRequester(
            RequestSpecs.auth_as_user(username, password),
            ResponseSpecs.request_returns_ok()
        ).get()

        assert new_profile.name == old_name