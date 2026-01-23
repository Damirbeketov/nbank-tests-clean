import random
import pytest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.configs.config import Config


@pytest.fixture(scope="function")
def user_request(api_manager: ApiManager, request) -> CreateUserRequest:
    mark = request.node.get_closest_marker("user_session")
    if mark:
        auth_index = int(mark.kwargs.get("auth", 0))
        return SessionStorage.get_user(auth_index)

    user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    return user_data

@pytest.fixture(scope='function')
def user_request_1(api_manager: ApiManager):
    user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    return user_data

@pytest.fixture(scope='function')
def user_request_2(api_manager: ApiManager):
    user_data: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_data)
    return user_data


@pytest.fixture
def admin_user_request() -> CreateUserRequest:
    return CreateUserRequest(
        username=Config.get("ADMIN_USERNAME"),
        password=Config.get("ADMIN_PASSWORD"),
        role=Config.get("ADMIN_ROLE"),
    )

@pytest.fixture
def deposit_amount():
    return round(random.uniform(0.1, 5000), 2)

@pytest.fixture
def invalid_deposit_amount():
    return round(random.uniform(5000.01, 10000), 2)

@pytest.fixture
def transfer_amount(deposit_amount):
    return round(random.uniform(0.1, deposit_amount), 2)

@pytest.fixture
def invalid_amount(deposit_amount):
    sum = round(random.uniform(0.01, 1000), 2)
    return deposit_amount + sum

@pytest.fixture
def invalid_account():
    return "ACC999999"

@pytest.fixture
def new_user_name():
    return "New Name"

@pytest.fixture(scope='function')
def current_user(user_factory):
    try:
        return SessionStorage.get_user(0)
    except Exception:
        user = user_factory()
        return user


@pytest.fixture(scope="function")
def user_factory(api_manager: ApiManager):
    def create_user() -> CreateUserRequest:
        user_data = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user_data)
        SessionStorage.add_users([user_data])
        return user_data

    yield create_user