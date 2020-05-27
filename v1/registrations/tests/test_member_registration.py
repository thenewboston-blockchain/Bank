from rest_framework import status
from thenewboston.accounts.manage import create_account
from thenewboston.blocks.block import generate_block
from thenewboston.verify_keys.verify_key import encode_verify_key

from v1.test_tools.test_base import TestBase


class TestMemberRegistration(TestBase):

    def test_list(self):
        """
        List member registrations
        """

        self.validate_get('/member_registrations', status.HTTP_200_OK)

    def test_post(self):
        """
        Register as a bank member
        """

        signing_key, account_number = create_account()
        encoded_account_number = encode_verify_key(verify_key=account_number)
        block = generate_block(
            account_number=account_number,
            balance_lock=encoded_account_number,
            payments=[
                {
                    'amount': 2,
                    'recipient': 'bank_001',
                },
                {
                    'amount': 2,
                    'recipient': 'validator_001',
                }
            ],
            signing_key=signing_key,
        )

        payload = {
            **block,
            'balance_lock': encoded_account_number
        }
        self.validate_post('/member_registrations', payload, status.HTTP_201_CREATED)
