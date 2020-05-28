## Member Registrations

Users are required to register at a bank before they are able to send transactions through that bank. If their 
registration is accepted they will be referred to as a "member" of that bank.

### POST /member_registrations

- `account_number` - account number of the registering account
- `balance_lock` - current balance lock for the above `account_number`
- `signature` - hex value of the signed `txs`
- `txs` - transactions for banks registration fee and validators transaction fee

Request:
```json
{
  "account_number": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
  "balance_lock": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
  "signature": "194308c4e6df46e17fa0b4fd2f460727d7a93eb622d2071a4aa53923f8fc5b88a750bd20eafe119cdb6f7e554dcb52c96b1a6d02ec614d3cefb2118bc4ea1d0d",
  "txs": [
    {
      "amount": 2,
      "balance_key": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
      "recipient": "bank_001"
    },
    {
      "amount": 2,
      "balance_key": "dd131b8345f7e1b4b1f61106058fc8ae037e8ee8529acc444fa7d1c189f8cfc6",
      "recipient": "validator_001"
    }
  ]
}
```

Response:
```json
{
  "id": "09e2b3ff-8680-4dab-b848-f2c1df9de0bb",
  "created_date": "2020-05-28T22:49:58.076873Z",
  "modified_date": "2020-05-28T22:49:58.076893Z",
  "fee": "2.0000000000000000",
  "status": "PENDING",
  "account_number": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
  "member": null
}
```

Upon successful member registration, the bank will create a bank block with the given data and send it to the validator
for validation. After successful validation, the validator will send a confirmation block back to the bank and the bank
will create the member and update the member registration status to accepted.

Bank block:
```json
{
  "block": {
    "account_number": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
    "signature": "194308c4e6df46e17fa0b4fd2f460727d7a93eb622d2071a4aa53923f8fc5b88a750bd20eafe119cdb6f7e554dcb52c96b1a6d02ec614d3cefb2118bc4ea1d0d",
    "txs": [
      {
        "amount": 2,
        "balance_key": "484b3176c63d5f37d808404af1a12c4b9649cd6f6769f35bdf5a816133623fbc",
        "recipient": "bank_001"
      },
      {
        "amount": 2,
        "balance_key": "dd131b8345f7e1b4b1f61106058fc8ae037e8ee8529acc444fa7d1c189f8cfc6",
        "recipient": "validator_001"
      }
    ]
  },
  "network_identifier": "d5356888dc9303e44ce52b1e06c3165a7759b9df1e6a6dfbd33ee1c3df1ab4d1",
  "signature": "e2fd7a34b27efde10548edcc693266339eec6e8346cc97b3d5c25d1c7167c48dda260081b622bc02e4f982cdd0c4f1cb7fd8e079dfa76c5625a1e85cfefeb203"
}
```
