#!/bin/bash

# API (v1) network nodes
python3 manage.py loaddata fixtures/bank.json
python3 manage.py loaddata fixtures/validator.json

# API (v1)
python3 manage.py loaddata fixtures/user.json
python3 manage.py loaddata fixtures/self_configuration.json
