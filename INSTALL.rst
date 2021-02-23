Local development environment setup
===================================

This section describes how to setup development environment for Debian-based distributions
(tested on Linux Mint 18.3 specifically)

Initial setup
+++++++++++++
Once initial setup is done only corresponding `Update`_ section should be performed
to get the latest version for development.

#. Install prerequisites::

    apt update
    apt install git

#. [if you have not configured it globally] Configure git::

    git config user.name 'Firstname Lastname'
    git config user.email 'youremail@youremail_domain.com'

#. Install prerequisites (
   as prescribed at https://github.com/pyenv/pyenv/wiki/Common-build-problems )::

    # TODO(dmu) MEDIUM: Remove those that are not really needed
    apt update && \
    apt install make build-essential libssl-dev zlib1g-dev libbz2-dev \
                libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
                libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

#. Install Docker according to https://docs.docker.com/engine/install/
   (known working: Docker version 19.03.2, build 6a30dfc)
#. Add your user to docker group::

    sudo usermod -aG docker $USER
    exit

#. Install Docker Compose according to https://docs.docker.com/compose/install/
   (known working: docker-compose version 1.27.4, build 40524192)

#. Fork https://github.com/thenewboston-developers/Bank repository (TODO(dmu) MEDIUM:
   Consider renaming the repository to `thenewboston-bank`)
#. Clone the fork::

    git clone git@bitbucket.org:<replace with you github name>/Bank.git

#. Add https://github.com/thenewboston-developers/Bank as upstream::

    cd Bank
    git remote add upstream git@github.com:thenewboston-developers/Bank.git
    git fetch upstream

#. Login to Github registry::

    # Use personal access token https://github.com/settings/tokens (github's credentials might not work)
    # Put the access token to ~/.github-pat
    cat ~/.github-pat | docker login docker.pkg.github.com -u <replace with you github name> --password-stdin

#. Create .env::

    cp dotenv .env
    vim .env
    # Set values:
    # - PUBLIC_IP_ADDRESS is an IP address of your docker host,
    # this should be 10/8 or 172.16/12 or 192.168/16 ip address (ex. local net ip address)
    # - ACCOUNT_NUMBER use `TNB Account Manager` app to generate a new account for test purposes

#. Install and configure `pyenv` according to https://github.com/pyenv/pyenv#basic-github-checkout
#. Install lowest supported Python version::

    pyenv install 3.9.2
    pyenv local 3.9.2  # run from the root of this repo (`.python-version` file should appear)

#. Install Poetry::

    # TODO(dmu) MEDIUM: Do we really need to pin `setuptools` and `wheel` at all or here?
    export PIP_REQUIRED_VERSION=21.0.1
    pip install pip==${PIP_REQUIRED_VERSION} && \
    pip install virtualenvwrapper && \
    pip install poetry==1.1.4 && \
    poetry config virtualenvs.path ${HOME}/.virtualenvs && \
    poetry run pip install pip==${PIP_REQUIRED_VERSION} && \
    poetry run pip install setuptools==53.0.0 && \
    poetry run pip install wheel==0.36.2

#. Setup local configuration::

    mkdir local && \
    cp config/templates/local.sh local/ && \
    vim local/local.sh

#. Do `Update`_ section
#. Initialize the project::

    . local/local.sh && poetry run python manage.py initialize_test_bank -ip ${PUBLIC_IP_ADDRESS}

Update
++++++
#. Install the project and dependencies::

    make install

#. [Optional] In case you plan to work on `thenewboston` in parallel then
   install it in editable (development) mode::

    poetry shell
    pip install 'toml>=0.10.2'
    cd <root of `thenewboston-python` repository>  # ex.: cd ../thenewboston-python
    # TODO(dmu) LOW: Fix `pip install -e .` failing with
    #                `ModuleNotFoundError: No module named 'setuptools'`
    python setup.py develop
    cd -

#. (in a separate terminal) Run dependency services::

    make up-dependencies-only

#. Run migrations::

    make migrate

Test
++++
#. Test::

    make up-dependencies-only  # run in a separate terminal
    . local/local.sh && make test

#. Test dockerized::

    make test-dockerized

#. Lint::

    make lint

Run
+++

Run Bank on host, other services with Docker
--------------------------------------------
#. (in a separate terminal) Run only dependency services with Docker::

    make up-dependencies-only

#. (in a separate terminal) Run Bank::

    make run

#. (in a separate terminal) Run Bank Celery::

    make run-celery

#. (in a separate terminal) Monitor Bank tasks::

    make monitor-bank-local

Run all services with Docker
----------------------------
#. Run all services with Docker::

    make up
    # Services availability on success (you can add them to your TNB Account Manager app)
    # http://$PUBLIC_IP_ADDRESS:8001 - PV
    # http://$PUBLIC_IP_ADDRESS:8002 - CV 1
    # http://$PUBLIC_IP_ADDRESS:8003 - CV 2
    # http://$PUBLIC_IP_ADDRESS:8004 - BANK

#. Monitor Bank tasks::

    make monitor-bank

Common
------
#. Monitor Validators' tasks::

    make monitor-pv
    make monitor-cv1
    make monitor-cv2

Build
+++++

#. Build docker image::

    make build
