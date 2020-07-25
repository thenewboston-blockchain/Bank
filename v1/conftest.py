import pytest

from v1.thirdparty.pytest.client import UserWrapper


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def anonymous_client():
    yield UserWrapper(None)
