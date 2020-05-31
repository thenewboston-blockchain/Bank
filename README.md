## Project Setup

Set required environment variables:
```
# Valid values are development, local, postgres_local, production, or staging
DJANGO_APPLICATION_ENVIRONMENT

# 64 character signing key used to authenticate network requests
NETWORK_SIGNING_KEY
```

Install and run Redis:
```
brew install redis
redis-server
```

Install required packages:
```
sudo pip3 install -r requirements/local.txt
```

Run Celery:
```
celery -A config.settings worker -l debug
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

## Developers

When adding a package, add to `requirements/base.in` and then :
```
bash scripts/compile_requirements.sh
```

Test account keys: https://docs.google.com/spreadsheets/d/1XzkE-KOOarIRkBZ_AoYIf7KpRkLEO7HOxOvLcWGxSNU/edit?usp=sharing
