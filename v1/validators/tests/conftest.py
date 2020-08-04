import pytest

from v1.third_party.factory.utils import build_json
from ..factories.validator import ValidatorFactory


@pytest.fixture
def validator_json_data():
    yield build_json(ValidatorFactory)


@pytest.fixture
def validators():
    yield ValidatorFactory.create_batch(100)
