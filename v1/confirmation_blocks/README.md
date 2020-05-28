## Confirmation Blocks

Confirmation blocks are blocks that have been signed by a validator as confirmation that it has been added to their 
blockchain. The general flow from bank member to confirmation block is as follows:

1. Members will send transactions to their bank
2. The bank will create a bank block from the received transactions and send that bank block to the validator
3. After successful validation, the validator will send a confirmation block back to the bank
