import pytest


@pytest.fixture(scope="function")
def valid_user_id() -> int:
    return 0


@pytest.fixture(scope="function")
def invalid_user_delete_id() -> int:
    return 1


@pytest.fixture(scope="function")
def testing_rate_limit() -> int:
    return 50
