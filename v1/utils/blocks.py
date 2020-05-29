from v1.bank_transactions.models.bank_transaction import BankTransaction
from v1.blocks.models.block import Block


def create_block_and_bank_transactions(block_data):
    """
    Create block and bank transactions
    """

    block = Block.objects.create(
        sender=block_data['account_number'],
        signature=block_data['signature']
    )

    bank_transactions = []

    for tx in block_data['txs']:
        bank_transaction = BankTransaction(
            amount=tx['amount'],
            balance_key=tx['balance_key'],
            block=block,
            recipient=tx['recipient'],
        )
        bank_transactions.append(bank_transaction)

    BankTransaction.objects.bulk_create(bank_transactions)

    return block
