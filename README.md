## Project Setup

Install required packages:
```shell script
sudo pip3 install -r requirements/local.txt
```

When adding a package, add to `requirements/base.in` and then :

```shell script
bash scripts/compile_requirements.sh
```

Initialize database:
```shell script
python3 manage.py migrate
```

## Running Tests

Run all tests:
```shell script
python3 manage.py test
```

Run all tests in parallel:
```shell script
python3 manage.py test --parallel
```

Run tests for individual app:
```shell script
python3 manage.py test v1/validators/
```
