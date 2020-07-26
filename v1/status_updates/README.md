## Status Updates

Banks will receive status updates from validators when certain events occur.

### POST /upgrade_notice

This is a notice from a previous confirmation validator that they are now a primary validator. If the requesting 
validator is more trusted than the banks current primary validator, the bank will switch to the new primary validator. 
This is because the banks always prefer the most trusted validator to be the primary validator for the network.

If the requesting validator is less trusted than the banks current primary validator, the bank will delete the 
requesting validator. This is because banks can only have one primary validator.
