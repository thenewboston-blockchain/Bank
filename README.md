# Community

Join the community to stay updated on the most recent developments, project roadmaps, and random discussions about
completely unrelated topics.

- [thenewboston.com](https://thenewboston.com/)
- [Slack](https://join.slack.com/t/thenewboston/shared_invite/zt-hkw1b98m-X3oe6VPX6xenHvQeaXQbfg)
- [reddit](https://www.reddit.com/r/thenewboston/)
- [Facebook](https://www.facebook.com/TheNewBoston-464114846956315/)
- [Twitter](https://twitter.com/bucky_roberts)
- [YouTube](https://www.youtube.com/user/thenewboston)

# Project Setup

Follow the steps below to set up the project on your environment. If you run into any problems, feel free to leave a 
GitHub Issue or reach out to any of our communities above.

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

To run all tests in parallel:
```
pytest -n auto
```

To monitor Celery tasks:
```
celery flower -A config.settings --address=127.0.0.1 --port=5555
```

## Local Development (Docker edition)

Run:
```
docker-compose up # add -d to detach from donsole
```

To run all tests in parallel:
```
docker-compose run app pytest -n auto
# or
docker-compose exec app pytest # if docker-compose run is running
```

To run tests with coverage report:
```
docker-compose run app pytest --cov=v1
# or
docker-compose exec app pytest --cov=v1 # if docker-compose run is running
```

To monitor Celery tasks:
```
docker-compose exec celery celery flower -A config.settings --address=127.0.0.1 --port=5555
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
