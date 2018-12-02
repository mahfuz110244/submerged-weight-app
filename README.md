# Django Project Misfit Technology Online Request Management

An example of Django project with basic user functionality.

## Functionality

- Log in
    - via email & password
    - with a remember me checkbox (optional)
- Create an account
- Log out
- Profile activation via email
- Reset password
- Remind a username
- Resend an activation code
- Change password
- Change email
- Change profile
- Everyone need to authenticate to use that application using following data: name, email,
profile picture.
- Every employee can see and create, update(before hr/manager approve) their request
- User who are from hr department can see all the requests and change the status in
either open/processed/hr reviewed
- User who are in managerial position can see request with “hr reviewed” status and make
that complete (processed)
- System can track who has processed the requests
- HR or manager can download request list as PDF file
- Super Admin can change user role from admin panel.
- Super Admin can manage all from admin panel.

## Install Necessary Packages

Open linux console and run the following command
```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python-pip python-dev libpq-dev postgresql postgresql-contrib supervisor nginx
```


## Create PostgreSQL DB and User

Change to the PostgreSQL system user:
```
sudo su postgres
psql
```

#### Create a database for the project misfit

```
CREATE DATABASE <dbname>;
```

#### Create a database user for the project:

```
CREATE USER <username> WITH PASSWORD '<password>';
```

#### Give the new user access to administer the new database:

```
GRANT ALL PRIVILEGES ON DATABASE dbname TO <username>;
```

#### Exit out of the PostgreSQL user’s shell session by typing:

```
\q
exit
```

### Go to the project directory:

```
cd /var/www/
```

Give permission to the user that he can do anything inside this directory without sudo
```
sudo chown username: /var/www
sudo chmod u+w /var/www
```

### Clone the project

```
git clone https://mahfuz110244@bitbucket.org/mahfuz110244/ticketing.git
cd ticketing
```

### Install dependencies & activate virtualenv

```
pip install virtualenv

virtualenv -p python3.6 venv3.6
source venv3.6/bin/activate
```

### Change database credential from settings.py in app/conf/development/ according to your requirements.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'misfit',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
### Change EMila credential from settings.py in app/conf/development/ for sending email

```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mahfuz.misfit@gmail.com'
EMAIL_HOST_PASSWORD = 'misfit1122'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'mahfuz.misfit@gmail.com'
```


### Install requirements inside virtual environment:
```
pip install -r requirements.txt
```

### Install WeasyPrint 43 dependencies for pdf:
```
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

### Make a console.loglogs file inside ticketing/logs:
```
mkdir logs
touch logs/console.log
```

### Configure the settings (connection to the database, connection to an SMTP server, and other options)

1. Edit `source/app/conf/development/settings.py` if you want to develop the project.

2. Edit `source/app/conf/production/settings.py` if you want to run the project in production.

### Apply migrations app wise

```
python manage.py makemigrations accounts
python manage.py migrate accounts
python manage.py makemigrations erequest
python manage.py migrate erequest
python manage.py makemigrations
python manage.py migrate
```

### Collect static files (only on a production server)

```
python manage.py collectstatic
```

### Running

### A development server

Just run this command:

```
python manage.py runserver
```

### Create Super User with misfit.tech domain to login in admin panel

```
python manage.py createsuperuser
```

### Run the unit test:

```
python manage.py test
```


### A production server

#### Create Gunicorn File gunicorn_start.sh inside source directory

```
#!/bin/bash

NAME="misfit"                            # Name of the application
DJANGODIR=/var/www/ticketing         # Django project directory
SOCKFILE=/var/www/ticketing/run/gunicorn.sock   # we will communicate using this unix socket
USER=root                                       # The user to run as
GROUP=webdata                                   # The group to run as
NUM_WORKERS=4                                   # How many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=app.settings             # Which settings file should Django use
DJANGO_WSGI_MODULE=app.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /var/www/ticketing/venv3.6/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE

```


Make the script executable:

```
chmod +x gunicorn_start.sh
```

#### Create Supervisor Configuration Files

Check Supervisor status:
```
sudo service supervisor status
```


If Supervisor is not running, then start Supervisor:
```
sudo service supervisor start
```

Create a Supervisor configuration file in /etc/supervisor/conf.d/ directory and name it misfit.conf:

```
[program:misfit]
command = /var/www/ticketing/gunicorn_start.sh                   ; Start app
user = root                                                                 ; User to run as
stdout_logfile = /var/www/ticketing/logs/gunicorn_supervisor.log ; Where to write log messages
redirect_stderr = true
```

Reread the configuration files and update Supervisor to start the project:
```
sudo supervisorctl reread
sudo supervisorctl update
```

It can also be started manually using:
```
sudo supervisorctl start misfit
```

#### Create Supervisor Configuration Files
Create Nginx server configuration in /etc/nginx/sites-enabled/ directory and name it misfit:
```
upstream app_server {
  server unix:/var/www/ticketing/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name ip_address or domain_name;

    client_max_body_size 4G;

    access_log /var/www/ticketing/logs/nginx_access.log;
    error_log /var/www/ticketing/logs/nginx_error.log;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        autoindex on;
        alias /var/www/ticketing/content/static/;
    }

    location /media/ {
        autoindex on;
        alias /var/www/ticketing/content/media/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /var/www/ticketing/content/static/;
    }
}
```

Enable the virtual servers and restart Nginx:
```
sudo ln -s /etc/nginx/sites-enabled/misfit /etc/nginx/sites-available/
sudo service nginx restart
```

#### Go to your ip address and see the home page
```
ip_address or domain
```

### Note:
Don't forget to create production database and change settings according to your requiremnets.