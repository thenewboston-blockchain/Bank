from rest_framework import serializers

from thenewboston_bank.accounts.models.account import Account
from thenewboston_bank.bank_transactions.models.bank_transaction import BankTransaction
from thenewboston_bank.blocks.models.block import Block
from thenewboston_bank.confirmation_blocks.models.confirmation_block import ConfirmationBlock


def create_bank_transactions(*, block, message):
    """Crete bank transactions from given block data"""
    bank_transactions = []

    for tx in message['txs']:
        bank_transaction = BankTransaction(
            amount=tx['amount'],
            block=block,
            fee=tx.get('fee', ''),
            recipient=tx['recipient']
        )
        bank_transactions.append(bank_transaction)

    BankTransaction.objects.bulk_create(bank_transactions)


def create_block_and_related_objects(block_data):
    """
    Create block, bank transactions, and account if necessary

    Returns block, block_created
    """
    account_number = block_data['account_number']
    message = block_data['message']
    signature = block_data['signature']
    balance_key = message['balance_key']

    block = Block.objects.filter(balance_key=balance_key).first()

    if block:

        # User is attempting to resend the same exact block
        if block.signature == signature:

            if ConfirmationBlock.objects.filter(block=block).exists():
                raise serializers.ValidationError('Block has already been confirmed')

            return block, False

        # User is using that balance key to send a new block (different Txs)
        BankTransaction.objects.filter(block=block).delete()
        create_bank_transactions(block=block, message=message)

        return block, False

    block = Block.objects.create(
        balance_key=balance_key,
        sender=account_number,
        signature=signature
    )
    create_bank_transactions(block=block, message=message)
    Account.objects.get_or_create(
        account_number=account_number,
        defaults={'trust': 0},
    )

    return block, True
