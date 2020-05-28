## Project Setup

Install required packages:
```
sudo pip3 install -r requirements/local.txt
```

When adding a package, add to `requirements/base.in` and then :

```
bash scripts/compile_requirements.sh
```

Initialize database:
```
python3 manage.py migrate
```

Set required environment variables:
```
# 64 character signing key
NETWORK_SIGNING_KEY
```

## Running Tests

Run all tests:
```
python3 manage.py test
```

Run all tests in parallel:
```
python3 manage.py test --parallel
```

Run tests for individual app:
```
python3 manage.py test v1/validators/
```

Testing:
```
# Bank
NETWORK_SIGNING_KEY: e5e5fec0dcbbd8b0a76c67204823678d3f243de7a0a1042bb3ecf66285cd9fd4
NID: d5356888dc9303e44ce52b1e06c3165a7759b9df1e6a6dfbd33ee1c3df1ab4d1

# PV
NETWORK_SIGNING_KEY: 6f812a35643b55a77f71c3b722504fbc5918e83ec72965f7fd33865ed0be8f81
NID: 3afdf37573f1a511def0bd85553404b7091a76bcd79cdcebba1310527b167521
```
