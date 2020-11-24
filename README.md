# Bank Setup guide 

### Install Dependencies:
```
sudo add-apt-repository universe
sudo apt -y update && sudo apt -y upgrade
sudo apt -y install build-essential nginx python3-pip redis-server
```
### Firewall:
```
sudo ufw app list
sudo ufw allow 'Nginx Full' && sudo ufw allow OpenSSH && sudo ufw enable
```
Verify that firewall is active and nginx is running:
```
sudo ufw status && systemctl status nginx
```

### Create a new user:
```
sudo adduser deploy
```
Allow this user to use sudo:
```
sudo visudo
```
Add following line into the opened file:
```
deploy ALL=(ALL) NOPASSWD:ALL
```
Switch to that new user:
```
sudo su deploy
```

### Setting up Postgres:
```
sudo apt install postgresql postgresql-contrib -y
```
```
sudo -u postgres psql
CREATE DATABASE thenewboston
CREATE USER deploy WITH PASSWORD 'password1234';
CREATE ROLE deploy WITH LOGIN;
  
ALTER ROLE deploy SET client_encoding TO 'utf8';
ALTER ROLE deploy SET default_transaction_isolation TO 'read committed';
  
ALTER ROLE deploy SET timezone TO 'UTC';
Or
ALTER ROLE deploy SET timezone = 'UTC';
  
GRANT ALL PRIVILEGES ON DATABASE thenewboston TO deploy;
\q
```

### Project Setup
Update /var/www/ permissions:
```
sudo chmod go+w /var/www
```

### Clone project to server and install dependencies:

```
git clone https://github.com/thenewboston-developers/Bank.git /var/www/Bank
cd /var/www/Bank/
```
### Setting up ENV variables
```
export DJANGO_APPLICATION_ENVIRONMENT='production'

A string with random chars
export SECRET_KEY='some random string'
```
```
sudo apt-get install libpq-dev -y
```
### Run project setup
```
sudo pip3 install -r requirements/production.txt
```

### NGINX
Create NGINX configuration:
```
sudo rm /etc/nginx/sites-available/default
sudo nano /etc/nginx/sites-available/default
```

Paste in the following and save:
```
upstream django {
    server 127.0.0.1:8001;
}

server {
    listen 80 default_server;
    server_name localhost;
    charset utf-8;
    client_max_body_size 75M;

    location /media {
        alias /var/www/Bank/media;
    }

    location /static {
        alias /var/www/Bank/static;
    }

    # Send all non-media requests to the Django server
    location / {
        proxy_pass http://django;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }

}
```
Test configuration:
```
sudo nginx -t
```
### Redis
Since we are running Ubuntu, which uses the systemd init system, change this to systemd:
```
sudo nano /etc/redis/redis.conf
```
Update the following line in the configuration and save file:
```
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd
```
Restart the Redis service to reflect the changes you made to the configuration file:
```
sudo systemctl restart redis.service
```
Check status to make sure Redis is running correctly:
```
sudo systemctl status redis
```

### Gateway Interface (daphne)
Create script to run daphne:
```
sudo nano /usr/local/bin/start_api.sh
```
Paste in the following and save:
```
#!/bin/bash

cd /var/www/Bank
daphne -p 8001 config.asgi:application
```
### Update permissions for the shell script:
```
sudo chmod a+x /usr/local/bin/start_api.sh
```
### Celery
Create a file to contain our environment variables:
```
cd /etc/
sudo mkdir bank
sudo mkdir /var/log/celery
sudo chown deploy /var/log/celery
sudo nano /etc/bank/environment
```
```
DJANGO_APPLICATION_ENVIRONMENT=production
NETWORK_SIGNING_KEY=yournetworksigningkey
POSTGRES_DB=thenewboston
POSTGRES_USER=deploy
POSTGRES_PASSWORD="posgrespassword"
SECRET_KEY='randomsecretkey'
```
Create celery env config:
```
sudo nano /etc/bank/celery.conf
```
```
CELERYD_NODES="w1 w2 w3"
CELERY_BIN="/usr/local/bin/celery"
CELERY_APP="config.settings"
CELERYD_MULTI="multi"
CELERYD_OPTS="--time-limit=1800 -Q:w1 celery -c:w1 2 -Q:w2 block_queue -P:w2 solo -Q:w3 confirmation_block_queue -P:w3 solo"
CELERYD_PID_FILE="/var/log/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="DEBUG"
DJANGO_APPLICATION_ENVIRONMENT=production
NETWORK_SIGNING_KEY=yournetworksigningkey
POSTGRES_DB=thenewboston
POSTGRES_USER=deploy
POSTGRES_PASSWORD="posgrespassword"
SECRET_KEY='randomsecretkey'
```
### Create service:
```
sudo nano /etc/systemd/system/api.service
```
```
[Unit]
Description = Service to run Django API
After = network.target

[Service]
EnvironmentFile = /etc/bank/environment
User = deploy
ExecStart = /usr/local/bin/start_api.sh

[Install]
WantedBy = multi-user.target
```
Update permissions for file:
```
sudo chmod a+x /etc/systemd/system/api.service
```
### Create service for celery:
```
sudo nano /etc/systemd/system/celery.service
```
```
[Unit]
Description=Bank Celery Service
After=network.target

[Service]
Type=forking
User=deploy
EnvironmentFile=/etc/bank/celery.conf
WorkingDirectory=/var/www/Bank
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target
```
### Reload systemd and enable both services:
```
sudo systemctl daemon-reload && sudo systemctl enable api && sudo systemctl enable celery
```
Verify it is enabled:
```
ls /etc/systemd/system/multi-user.target.wants/
```
### System Services
Start API service, restart NGINX, and verify services are active:
```
sudo systemctl start api && sudo systemctl start celery && sudo systemctl restart nginx
```
### Check the status of the services:
```
sudo systemctl status api celery nginx redis
```
### Static Files and Application Configuration
Set environment variable:
```
nano ~/.profile
```
```
export DJANGO_APPLICATION_ENVIRONMENT=production
export NETWORK_SIGNING_KEY=yournetworksigningkey
export POSTGRES_DB=thenewboston
export POSTGRES_USER=deploy
export POSTGRES_PASSWORD="posgrespassword"
```
Log out and log back in:
```
logout
su - deploy
printenv
```
### Set up database:
```
cd /var/www/Bank/
python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
```
### Initialize Initialize server as bank:
```
python3 manage.py initialize_bank
```
If setting up confirmation validator, run this script to connect to the primary validator:
```
python3 manage.py set_primary_validator
```
Verify everything is working correctly by visiting:
```
http://[IP_ADDRESS]/config
```
### Troubleshooting
Check the status of the services:
```
sudo systemctl status api celery nginx redis
```
View the logs:
```
sudo journalctl -u api.service
sudo journalctl -u celery.service
sudo journalctl -u nginx.service
```

### Errors:
If you run into a secret SECRET_KEY error you need to redo the command 
```
export SECRET_KEY='some random string'
```
If it starts talking about not being able to login to postgres username login.
You will need to go into the base.py file and change the forms in the file for postgres.
```
nano var/www/Bank/config/settings/base.py
```
