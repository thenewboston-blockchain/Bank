import pytest

from ..factories.validator_confirmation_service import ValidatorConfirmationServiceFactory


@pytest.fixture
def validator_confirmation_services():
    yield ValidatorConfirmationServiceFactory.create_batch(100)
