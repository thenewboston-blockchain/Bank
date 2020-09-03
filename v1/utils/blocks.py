from rest_framework import serializers

from v1.bank_transactions.models.bank_transaction import BankTransaction
from v1.blocks.models.block import Block
from v1.confirmation_blocks.models.confirmation_block import ConfirmationBlock


def create_bank_transactions(*, block, message):
    """
    Crete bank transactions from given block data
    """

    bank_transactions = []

    for tx in message['txs']:
        bank_transaction = BankTransaction(
            amount=tx['amount'],
            block=block,
            recipient=tx['recipient']
        )
        bank_transactions.append(bank_transaction)

    BankTransaction.objects.bulk_create(bank_transactions)


def create_block_and_bank_transactions(block_data):
    """
    Create block and bank transactions
    Returns block, created
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

    return block, True
