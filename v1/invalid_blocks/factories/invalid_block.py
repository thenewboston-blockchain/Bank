from factory import Faker, SubFactory
from thenewboston.constants.network import BLOCK_IDENTIFIER_LENGTH
from thenewboston.factories.created_modified import CreatedModifiedFactory

from v1.blocks.factories.block import BlockFactory
from v1.validators.factories.validator import ValidatorFactory
from ..models.invalid_block import InvalidBlock


class InvalidBlockFactory(CreatedModifiedFactory):
    block = SubFactory(BlockFactory)
    block_identifier = Faker('text', max_nb_chars=BLOCK_IDENTIFIER_LENGTH)
    confirmation_validator = SubFactory(ValidatorFactory)
    primary_validator = SubFactory(ValidatorFactory)

    class Meta:
        model = InvalidBlock
