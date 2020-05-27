import os
from os.path import join, normpath

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIXTURES_ROOT = join(ROOT, 'fixtures')

PATHS = [

    # API (v1) network nodes
    'bank.json',
    'validator.json',

    # API (v1)
    'user.json',
    'self_configuration.json',

]

FIXTURES = [normpath(join(FIXTURES_ROOT, path)) for path in PATHS]
