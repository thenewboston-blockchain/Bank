import pytz
from factory import Faker
from thenewboston.models.confirmation_service import ConfirmationService

from v1.third_party.thenewboston.factories.created_modified import CreatedModifiedFactory


class ConfirmationServiceFactory(CreatedModifiedFactory):
    end = Faker('date_time', tzinfo=pytz.utc)
    start = Faker('date_time', tzinfo=pytz.utc)

    class Meta:
        model = ConfirmationService
