FROM python:3.8

WORKDIR /opt/project

COPY . .

RUN set -x; \
    python3 -m pip install pip-tools; \
    python3 -m pip install --no-cache-dir -r requirements/local.txt; \
    test -e thenewboston.tar.gz && python3 -m pip install thenewboston.tar.gz; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache
