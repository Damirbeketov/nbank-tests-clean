import pytest
import logging
from typing import Any, List

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.fixture
def created_objects():
    objects: List[Any] = []
    yield objects

    cleanup_objects(objects)

def cleanup_objects(objects: List[Any]):
    api_manager = ApiManager(objects)

    for obj in objects:
        try:
            if isinstance(obj, CreateUserRequest):
                profile = api_manager.user_steps.get_profile(obj)
                api_manager.admin_steps.delete_user(profile.id)

            elif isinstance(obj, CreateUserResponse):
                api_manager.admin_steps.delete_user(obj.id)

        except:
            logging.warning(f"Object type: {type(obj)} is not deleted")