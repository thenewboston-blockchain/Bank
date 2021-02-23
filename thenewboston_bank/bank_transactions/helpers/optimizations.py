def optimize_bank_transaction_list(bank_transactions):
    """Append related objects using select_related and prefetch_related"""
    return bank_transactions.select_related('block')
