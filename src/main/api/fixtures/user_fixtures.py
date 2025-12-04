import random
import pytest
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager


@pytest.fixture(scope='function')
def user_request(api_manager: ApiManager):
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
def admin_user_request():
    return CreateUserRequest(username='admin', password='admin', role='ADMIN')

@pytest.fixture
def deposit_amount():
    return round(random.uniform(0.1, 5000), 2)

@pytest.fixture
def transfer_amount(deposit_amount):
    return round(random.uniform(0.1, deposit_amount), 2)

@pytest.fixture
def invalid_amount(deposit_amount):
    sum = round(random.uniform(0.01, 1000), 2)
    return deposit_amount + sum