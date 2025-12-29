from __future__ import annotations
from typing import List, Optional

from src.main.api.models.create_user_request import CreateUserRequest


class SessionStorage:
    _users: List[CreateUserRequest] = []
    _current_user: Optional[CreateUserRequest] = None

    @classmethod
    def add_users(cls, users: List[CreateUserRequest]) -> None:
        cls._users.extend(list(users))

    @classmethod
    def set_user(cls, user: CreateUserRequest) -> None:
        cls._current_user = user

    @classmethod
    def get_current_user(cls) -> CreateUserRequest:
        if cls._current_user is None:
            raise RuntimeError("No current user set in SessionStorage")
        return cls._current_user

    @classmethod
    def get_user(cls, index: int = 0) -> CreateUserRequest:
        if index >= len(cls._users):
            raise IndexError(
                f"User index (0-based) out of range: {index}; total={len(cls._users)}"
            )
        return cls._users[index]

    @classmethod
    def clear(cls) -> None:
        cls._users.clear()
        cls._current_user = None