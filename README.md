# Django Project IDARE

An example of Django project with basic input output functionality.

## Functionality

- Calculate Submerged Weighted

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

### Clone the project and go to project folder

```
git clone https://github.com/mahfuz110244/submerged-weight-app.git
cd submerged-weight-app
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
        'NAME': 'dbname',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```


### Install requirements inside virtual environment:
```
pip install -r requirements.txt
```


### Apply migrations

```
python manage.py makemigrations
python manage.py migrate
```

### Running in local machine

Just run this command:

```
python manage.py runserver
```

### Go to following url in your browser and Calculate data according to your data

```
http://127.0.0.1:8000/
```