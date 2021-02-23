# Project Setup

Follow the steps below to set up the project on your environment. If you run into any problems, feel free to leave a 
GitHub Issue or reach out to any of our communities above.
(RECOMMENDED: see `INSTALL.rst` for detailed step-by-step setup for Debian-based distributions)

## Local Development (Docker edition)

You need to have [Docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed

Copy `dotenv` to `.env` 

Open .env and edit settings

- `PUBLIC_IP_ADDRESS` is an IP address of your docker host, this should be 10/8 or 172.16/12 or 192.168/16 ip address (ex. local net ip address)
- `ACCOUNT_NUMBER` use `TNB Account Manager` app to generate a new account for test purposes

Login to Github's registry 
```shell
docker login docker.pkg.github.com
```
Use your github's credentials or personal access token if you have 2FA configured.

Run:
```shell
docker-compose up # add -d to detach from console
```

This will start a dev network to work with, network consists of Bank, PV, 2x CVs and all the needed services (celery, db, redis).

On a first run it will take some time to provision and configure test network settings.

If something failed, deleting `postgresql-data` and `redis-data` volumes might solve the issue (refer to `docker volume` cli), and try previous command again.

As a result
```
http://$PUBLIC_IP_ADDRESS:8004 - BANK
http://$PUBLIC_IP_ADDRESS:8001 - PV
http://$PUBLIC_IP_ADDRESS:8002 - CV 1
http://$PUBLIC_IP_ADDRESS:8003 - CV 2
```

You can add those to your TNB Account Manager app

### For Python developers (Docker edition)
To run all tests in parallel:
```shell
docker-compose run bank pytest -n auto
# or
docker-compose exec bank pytest # if docker-compose run is running
```

To monitor Celery tasks:
```shell
# For BANK
docker-compose exec celery_bank celery flower -A config.settings --port=5559
# For PV
docker-compose exec celery_pv celery flower -A config.settings --port=5556
# For CV n. 1
docker-compose exec celery_cv1 celery flower -A config.settings --port=5557
# For CV n. 2
docker-compose exec celery_cv2 celery flower -A config.settings --port=5558
```

## Windows (without docker)

This guide targets a unix environment however it is possible to perform this setup on Windows by installing Cygwin 
[here](https://cygwin.com/install.html).

When installing Cygwin ensure you add the following packages in the setup wizard choosing the most up-to-date version for each:

* python3
* python3-devel
* pip3
* gcc-core
* libffi-devel
* make
* python38-wheel
* libintl-devel
  
Once installed use Cygwin for all your command-line operations.

*This is because one of the dependencies, uWSGI, does not provide Windows support directly.*

## Steps (without docker)

Set required environment variables:
```
# Valid values are development, local, postgres_local, production, or staging
export DJANGO_APPLICATION_ENVIRONMENT='local'

# 64 character signing key used to authenticate network requests
export NETWORK_SIGNING_KEY='6f812a35643b55a77f71c3b722504fbc5918e83ec72965f7fd33865ed0be8f81'

# A string with random chars
export SECRET_KEY='some random string'
```

Install Redis:
```
brew install redis
```

Install Python 3.9.2 or higher.

Install required packages:
```
pip3 install virtualenvwrapper && \
pip3 install poetry==1.1.4 && \
poetry config virtualenvs.path ${HOME}/.virtualenvs && \
poetry install
```

To initialize the project:
```
python3 manage.py migrate
python3 manage.py initialize_test_bank -ip [IP ADDRESS]
```

## Local Development (without Docker)

Run Redis:
```
redis-server
```

Run Celery (run each as a separate process):
```
celery -A config.settings worker -l debug
```

To monitor Celery tasks:
```
celery flower -A config.settings --address=127.0.0.1 --port=5555
```

## Developers

To watch log files:
```shell
tail -f logs/warning.log -n 10
```

To run all tests in parallel:
```shell
pytest -n auto
```

To generate documentation:
```shell
cd docs
make html
```

## Community

Join the community to stay updated on the most recent developments, project roadmaps, and random discussions about completely unrelated topics.

- [thenewboston.com](https://thenewboston.com/)
- [Discord](https://discord.gg/thenewboston)
- [Facebook](https://www.facebook.com/TheNewBoston-464114846956315/)
- [Instagram](https://www.instagram.com/thenewboston_official/)
- [LinkedIn](https://www.linkedin.com/company/thenewboston-developers/)
- [Reddit](https://www.reddit.com/r/thenewboston/)
- [Twitch](https://www.twitch.tv/thenewboston/videos)
- [Twitter](https://twitter.com/thenewboston_og)
- [YouTube](https://www.youtube.com/user/thenewboston)

## Donate

All donations will go to thenewboston to help fund the team to continue to develop the community and create new content.

| Coin | Address |
|-|-|
| ![thenewboston Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/thenewboston.png) | b6e21072b6ba2eae6f78bc3ade17f6a561fa4582d5494a5120617f2027d38797 |
| ![Bitcoin Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/bitcoin.png) | 3GZYi3w3BXQfyb868K2phHjrS4i8LooaHh |
| ![Ethereum Logo](https://github.com/thenewboston-developers/Website/raw/development/src/assets/images/ethereum.png) | 0x0E38e2a838F0B20872E5Ff55c82c2EE7509e6d4A |

## License

thenewboston is [MIT licensed](http://opensource.org/licenses/MIT).
