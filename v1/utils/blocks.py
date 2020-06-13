from v1.bank_transactions.models.bank_transaction import BankTransaction
from v1.blocks.models.block import Block


def create_block_and_bank_transactions(block_data):
    """
    Create block and bank transactions
    """

    message = block_data['message']

    block = Block.objects.create(
        balance_key=message['balance_key'],
        sender=block_data['account_number'],
        signature=block_data['signature']
    )

    bank_transactions = []
    message = block_data['message']

    for tx in message['txs']:
        bank_transaction = BankTransaction(
            amount=tx['amount'],
            block=block,
            recipient=tx['recipient']
        )
        bank_transactions.append(bank_transaction)

    BankTransaction.objects.bulk_create(bank_transactions)

    return block
