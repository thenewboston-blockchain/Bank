## Bank Registrations

Banks must also register with validators before they are accepted onto the network by that validator. This is done in a 
similar fashion to the registration process between user accounts and banks. To register, banks will pay a registration 
fee to the validator. The validator will then place the registration in a "pending" state as it performs a network 
background check of the applying bank. During this process, validators will check the bank's trust level with other 
existing banks. Banks must also prove that they are configured properly to act as a bank node. This is done through the 
ability to act as a server by responding properly to network requests made from the validator to the bank's IP address. 
This verification prevents end users from acting as banks by sending transactions directly to the validator.

### PATCH /bank_registrations

- `message` - status to indicate the result of the bank registration
- `network_identifier` - network identifier of the primary validator
- `signature` - hex value of the signed `message`

Request:
```json
{
  "message": {
    "status": "ACCEPTED"
  },
  "network_identifier": "3afdf37573f1a511def0bd85553404b7091a76bcd79cdcebba1310527b167521",
  "signature": "11773d39c58cf99f60c0bda385a5ac1135c0c0246554cedded78ce68896c00ac851413543d77aa6aeefc76ef2f9962301a370c934be5c0d88d3b8cc0e6fc0f09"
}
```

Response:
```json
{
  "id": "afce31d3-5c55-479c-8e42-eff28358b113",
  "created_date": "2020-06-19T21:51:41.136479Z",
  "modified_date": "2020-06-19T22:17:56.705678Z",
  "fee": "0.0000000000000001",
  "status": "ACCEPTED",
  "validator": "a8101b03-15ad-42fc-8e64-2de24b850e0e"
}
```
