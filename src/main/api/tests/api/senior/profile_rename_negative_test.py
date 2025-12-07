import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.profile_request import ProfileRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


import pytest

@pytest.mark.api
class TestProfileRenameNegative:
    @pytest.mark.parametrize(
        "name, expected_message",
        [
            ('UserName', 'Name must contain two words with letters only'),
            ('User! Name', 'Name must contain two words with letters only'),
            ('User Name1', 'Name must contain two words with letters only'),
            ('user name.', 'Name must contain two words with letters only'),
            ('User', 'Name must contain two words with letters only'),
            ('User Name User', 'Name must contain two words with letters only'),
            (' User Name', 'Name must contain two words with letters only'),
            ('User Name ', 'Name must contain two words with letters only'),
            (' User Name ', 'Name must contain two words with letters only'),
            ('', 'Name must contain two words with letters only'),
            (' ', 'Name must contain two words with letters only'),
            ('! ?', 'Name must contain two words with letters only'),
        ]
    )
    @pytest.mark.usefixtures("api_manager", "user_request")
    def test_invalid_rename(self, api_manager, user_request, name, expected_message):
        api_manager.user_steps.login(user_request)
        old_profile = api_manager.user_steps.get_customer_profile(user_request)
        old_name = old_profile.name

        api_manager.user_steps.profile_rename_negative(
            user_request,
            name,
            expected_message
        )

        # проверяем что имя не изменилось
        new_profile = api_manager.user_steps.get_customer_profile(user_request)
        assert new_profile.name == old_name

