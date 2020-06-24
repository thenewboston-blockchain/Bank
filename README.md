## Project Setup

The development environment uses a private repository. To be able to install this as a dependency you will need to add
an SSH key to your GitHub account. 

```
# Check if you already have an SSH key
cat ~/.ssh/id_rsa.pub

# Create an SSH key if you do not already have one
ssh-keygen -t rsa

# Copy to clipboard (Mac)
pbcopy < ~/.ssh/id_rsa.pub
```

Add your SSH key to GitHub: https://github.com/settings/keys

Set required environment variables:
```
# Valid values are development, local, postgres_local, production, or staging
DJANGO_APPLICATION_ENVIRONMENT='local'

# 64 character signing key used to authenticate network requests
NETWORK_SIGNING_KEY='e5e5fec0dcbbd8b0a76c67204823678d3f243de7a0a1042bb3ecf66285cd9fd4'
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
python3 manage.py test --parallel
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

Test account keys: https://docs.google.com/spreadsheets/d/1XzkE-KOOarIRkBZ_AoYIf7KpRkLEO7HOxOvLcWGxSNU/edit?usp=sharing
