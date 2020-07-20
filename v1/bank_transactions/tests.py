import secrets

from decimal import Decimal
from http import HTTPStatus

from django.urls import reverse

from rest_framework.test import APITestCase

from v1.bank_transactions.models.bank_transaction import BankTransaction
from v1.blocks.models.block import (
    Block,
    BALANCE_LOCK_LENGTH,
    SIGNATURE_LENGTH,
)


class FilterTests(APITestCase):
    """
    Tests for `BankTransactionView` filtering.
    """
    URL = reverse('bank_transactions:banktransaction-list')

    def setUp(self):
        self.bank1 = 'bank_001'
        self.bank2 = 'bank_002'
        self.bank3 = 'bank_003'
        self.bank4 = 'bank_004'
        bank1_block = Block.objects.create(
            balance_key=secrets.token_urlsafe(BALANCE_LOCK_LENGTH),
            sender=self.bank1,
            signature=secrets.token_urlsafe(SIGNATURE_LENGTH),
        )
        bank2_block = Block.objects.create(
            balance_key=secrets.token_urlsafe(BALANCE_LOCK_LENGTH),
            sender=self.bank2,
            signature=secrets.token_urlsafe(SIGNATURE_LENGTH),
        )
        for _ in range(5):
            # Create 5 `BankTransaction` instances for `bank3` recipient.
            BankTransaction.objects.create(
                block=bank1_block,
                amount=Decimal(100),
                recipient=self.bank3
            )
        for _ in range(7):
            # Create 7 `BankTransaction` instances for `bank4` recipient.
            BankTransaction.objects.create(
                block=bank2_block,
                amount=Decimal(100),
                recipient=self.bank4
            )

    def test_list_no_filter(self):
        params = {}
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.data), 12)

    def test_filter_recipient(self):
        params = {
            'recipient': self.bank3,
        }
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.data), 5)

        params = {
            'recipient': self.bank4,
        }
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.data), 7)

    def test_filter_sender(self):
        """
        Test that there are 5 instances where `bank1` is the `Block` sender.
        """
        params = {
            'block__sender': self.bank1,
        }
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.data), 5)

    def test_filter_account_number(self):
        """
        Test filtering both `recipient` and `block__sender` with
        `account_number` query param.
        """
        params = {
            'account_number': self.bank4,
        }
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        # Assert  data for `bank4` as recipient
        self.assertEqual(len(res.data), 7)

        # Create data for `bank4` as sender
        bank4_block = Block.objects.create(
            balance_key=secrets.token_urlsafe(BALANCE_LOCK_LENGTH),
            sender=self.bank4,
            signature=secrets.token_urlsafe(SIGNATURE_LENGTH),
        )
        for _ in range(3):
            BankTransaction.objects.create(
                block=bank4_block,
                amount=Decimal(100),
                recipient=self.bank1
            )
        res = self.client.get(self.URL, params)
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertEqual(len(res.data), 10)
