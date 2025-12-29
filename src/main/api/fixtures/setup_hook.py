import pytest
from playwright.sync_api import Page

from src.main.api.utils.normalize_browsers import norm_browser_name
from src.main.ui.pages.login_page import LoginPage
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert

@pytest.fixture(autouse=True, scope="function")
def user_session_extension(request, page, user_factory):
    mark = request.node.get_closest_marker("user_session")
    if not mark:
        yield
        return

    count = max(int(mark.args[0]), 1)
    auth_index = int(mark.kwargs.get("auth", 0))

    users = [user_factory() for _ in range(count)]
    SessionStorage.add_users(users)

    lp = LoginPage(page)

    lp.auth_as_user(users[auth_index])

    yield

    SessionStorage.clear()



@pytest.fixture(autouse=True)
def admin_session_autologin(
    request: pytest.FixtureRequest,
    page: Page,
    admin_user_request: CreateUserRequest
):
    mark = request.node.get_closest_marker("admin_session")
    if not mark:
        return

    LoginPage(page).auth_as_user(admin_user_request)


@pytest.fixture(autouse=True)
def browser_match_guard(request):
    mark = request.node.get_closest_marker("browsers")
    if not mark:
        return

    allowed = {norm_browser_name(str(x)) for x in (mark.args or ())}
    if not allowed:
        return

    try:
        current = request.getfixturevalue("browser_name")
    except Exception:
        return

    if norm_browser_name(str(current)) not in allowed:
        pytest.skip(f"Пропущен: текущий браузер '{current}' не в {sorted(allowed)}")