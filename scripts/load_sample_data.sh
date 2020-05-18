#!/bin/bash

python3 manage.py loaddata fixtures/user.json
python3 manage.py loaddata fixtures/self_configuration.json
