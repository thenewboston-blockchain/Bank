#!/usr/bin/env python
"""Generate account keys"""
from nacl.encoding import HexEncoder
from thenewboston.accounts.manage import create_account

private_key, public_key = create_account()
private_key = private_key.encode(encoder=HexEncoder).decode('utf-8')
public_key = public_key.encode(encoder=HexEncoder).decode('utf-8')
