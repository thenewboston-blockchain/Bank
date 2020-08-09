import pytest

from ..factories.block import BlockFactory


@pytest.fixture
def blocks():
    yield BlockFactory.create_batch(100)
