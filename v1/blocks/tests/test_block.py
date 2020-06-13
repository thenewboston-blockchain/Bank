from rest_framework import status
from thenewboston.accounts.manage import create_account
from thenewboston.blocks.block import generate_block
from thenewboston.verify_keys.verify_key import encode_verify_key

from v1.members.models.member import Member
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.test_tools.helpers import random_account_number
from v1.test_tools.test_base import TestBase


class TestBlock(TestBase):

    def test_list(self):
        """
        List blocks
        """

        self.validate_get('/blocks', status.HTTP_200_OK)

    def test_post(self):
        """
        Create block
        """

        signing_key, account_number = create_account()
        encoded_account_number = encode_verify_key(verify_key=account_number)
        Member.objects.create(account_number=encoded_account_number, trust=50)

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        primary_validator = self_configuration.primary_validator

        block = generate_block(
            account_number=account_number,
            balance_lock=encoded_account_number,
            signing_key=signing_key,
            transactions=[
                {
                    'amount': float(self_configuration.default_transaction_fee),
                    'recipient': self_configuration.account_number
                },
                {
                    'amount': float(primary_validator.default_transaction_fee),
                    'recipient': primary_validator.account_number
                },
                {
                    'amount': self.fake.pyfloat(min_value=1, max_value=100, positive=True, right_digits=4),
                    'recipient': random_account_number()
                }
            ]
        )

        self.validate_post('/blocks', block, status.HTTP_201_CREATED)
