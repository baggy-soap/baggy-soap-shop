# Baggy Soap Shop Website Local Setup

A brief setup to get the Baggy Soap Shop website running locally.
Please note, this readme is written for Linux and needs updating if
you want to use a Mac.

## Requirements

- Python (v3.6.x) / pip / virtualenv / virtualenvwrapper
- Postgres

## Installing requirements

1) Install Python 3.6.4

```
$ sudo apt-get install build-essential checkinstall
$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
$ cd /usr/src
$ sudo wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
$ sudo tar xzf Python-3.6.4.tgz
$ cd Python-3.6.4
$ sudo ./configure --enable-optimizations
$ sudo make altinstall
```

2) Install virtualenvwrapper and make virtualenv

```
$ sudo apt-get install python3-pip
$ sudo pip3 install virtualenvwrapper
```

Add to .bashrc

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/workspace
source /usr/local/bin/virtualenvwrapper.sh
```

Reload shell startup file:

```
$ source ~/.bashrc
```

Make virtualenv:

```
$ mkvirtualenv --python=python3 baggy-soap
```

3) Set up PostgreSQL database

Install new version: 

https://www.postgresql.org/download/linux/ubuntu/

Create user and DB:

```
$ sudo su - postgres
$ psql
# CREATE USER baggysoapdb WITH PASSWORD 'khAk8ZTguB4zS3';
# CREATE DATABASE baggysoapshop;
# GRANT ALL PRIVILEGES ON DATABASE baggysoapshop to baggysoapdb;
# \q
$ exit
```

## Installation

To install this project, follow these steps:

```
$ git clone https://github.com/baggy-soap/baggy-soap-shop.git
$ cd baggysoapshop/
$ pip3 install -r requirements.txt
$ cp .env.example .env
$ python3 manage.py migrate
```

To create yourself as an admin user on the Django Oscar website, do the following:

```
$ python3 manage.py createsuperuser
```

Choose a username and password, and use your baggysoap.co.uk email address.

## Running Locally

Prior to running the server, you will need to update your .env file to contain the correct values for api keys and
passwords, etc.

```
$ workon baggy-soap
$ python3 manage.py runserver
```

Go to http://localhost:8000 to verify the website is running, 
and http://localhost:8000/dashboard to test your login credentials.

## Deployment to Heroku

Before deploying to Heroku for the first time, you will need to add the remotes for staging and production, and login
to Heroku.

    $ git remote add staging https://git.heroku.com/baggy-soap-staging.git
    $ git remote add production https://git.heroku.com/baggy-soap-production.git
    $ heroku login

This is the process for deploying a branch to Heroku (staging and production). If working on master directly, you can 
simply push `master` to staging rather than `<branch>:master`

    # Do due dilligence -------------------------------------------------------------
    $ pythons manage.py makemigrations # Check no migrations are missing from the codebase

    # Release to staging ------------------------------------------------------------
    $ heroku pg:backups capture --app baggy-soap-staging
    $ git push staging <branch>:master
    $ heroku run python manage.py migrate --app baggy-soap-staging

    # Release to production ---------------------------------------------------------
    $ git checkout master
    $ git merge <branch>
    $ heroku pg:backups capture --app baggy-soap-production
    $ git push production master
    $ heroku run python manage.py migrate --app baggy-soap-production

If you need to roll back due to a bad deployment/migration you can use the backup created before the push.
NOTE: These rollback commands have not been tested, use with caution and update the README.

    $ heroku rollback
    $ heroku pg:backups restore <backup_name> DATABASE_URL --app baggy-soap-staging

## Get a copy of the staging database

Before pushing model changes to staging, it is wise to obtain a copy of the staging database and test the migrations
locally. This is how to do so.

    $ sudo su - postgres
    $ /usr/lib/postgresql/10/bin/pg_dump <database_url> > staging.sql
    $ createdb baggysoapshopstaging
    $ psql baggysoapshopstaging < staging.sql
    $ psql
    # GRANT ALL PRIVILEGES ON DATABASE baggysoapshopstaging to baggysoapdb;
    # \q

    # Set extra privileges to prevent access errors --------------------------------
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to baggysoapdb;"
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to baggysoapdb;"
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to baggysoapdb;"
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA information_schema to baggysoapdb;"
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA information_schema to baggysoapdb;"
    $ psql baggysoapshopstaging -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA information_schema to baggysoapdb;"
    $ exit

## Adding and upgrading Python dependencies

We use [`pip-tools`](https://github.com/jazzband/pip-tools) to manage Python dependencies.

To add a new direct dependency, add it to `requirements.in` and run `pip-compile`. `requirements.txt` will be recreated, 
pinning an exact version of the new package and all its dependencies.

To upgrade a particular package to the latest, you can run (for example) `pip-compile -P celery`
to regenerate a new `requirements.txt` with the latest package and valid dependencies while leaving
other packages at their current versions!
