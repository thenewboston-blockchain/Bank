FROM python:3.8

WORKDIR /opt/project

COPY requirements/local.txt .

RUN set -x; \
    python3 -m pip install pip-tools; \
    python3 -m pip install --no-cache-dir -r local.txt; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache
