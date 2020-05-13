## Project Setup

Install required packages:
```commandline
sudo pip3 install -r requirements/local.txt
```

When adding a package, add to `requirements/base.in` and then :

```commandline
bash scripts/compile_requirements.sh
```

Initialize database:
```commandline
python3 manage.py migrate
```

## Running Tests

Run all tests:
```commandline
python3 manage.py test
```

Run all tests in parallel:
```commandline
python3 manage.py test --parallel
```

Run tests for individual app:
```commandline
python3 manage.py test v1/validators/
```
