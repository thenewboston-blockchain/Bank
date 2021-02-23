import pytest
from thenewboston.third_party.factory.utils import build_json

from ..factories.account import AccountFactory


@pytest.fixture
def account_fake_data():
    yield build_json(AccountFactory)


@pytest.fixture
def accounts():
    yield AccountFactory.create_batch(100)
