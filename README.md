## Project Setup

Clone this repository and cd into it:
```
git clone https://github.com/thenewboston-developers/Bank.git
cd Bank
```

Set required environment variables:
```
# Valid values are development, local, postgres_local, production, or staging
export DJANGO_APPLICATION_ENVIRONMENT='local'

# 64 character signing key used to authenticate network requests
export NETWORK_SIGNING_KEY='e5e5fec0dcbbd8b0a76c67204823678d3f243de7a0a1042bb3ecf66285cd9fd4'
```

Install Redis:
```
brew install redis
```

Create a virtual environment with Python 3.6 or higher.

Install required packages:
```
pip3 install -r requirements/local.txt
```

## Local Development

Run Redis:
```
redis-server
```

Run Celery:
```
celery -A config.settings worker -l debug
```

To run all tests:
```
pytest
```

To monitor Celery tasks:
```
celery flower -A config.settings --address=127.0.0.1 --port=5555
```

## Developers

To watch log files:
```commandline
tail -f logs/warning.log -n 10
```

When adding a package, add to `requirements/base.in` and then :
```
bash scripts/compile_requirements.sh
```
