from thenewboston.accounts.manage import create_account
from thenewboston.verify_keys.verify_key import encode_verify_key


def random_account_number():
    """
    Generate random encoded account number for testing
    """

    _, account_number = create_account()
    return encode_verify_key(verify_key=account_number)
