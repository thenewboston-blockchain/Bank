import pytest
from thenewboston.third_party.factory.utils import build_json

from ..factories.validator import ValidatorFactory


@pytest.fixture
def validator_fake_data():
    yield build_json(ValidatorFactory)


@pytest.fixture
def validators():
    yield ValidatorFactory.create_batch(100)
