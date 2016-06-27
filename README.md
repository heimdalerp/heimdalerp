# HeimdalERP

Heimdal is a free and opensource ERP solution based on Django REST Framework.

It is named after Heimdallr, a god of Norse mythology.
Heimdallr is attested as possessing foreknowledge, keen eyesight and hearing, and is described as "the whitest of the gods".
He guards Bifrost, the bridge which connects the human world with Asgard, the gods' world.
It is said that he brings the gift of the gods to mankind.

## 1. Install from source

### 1.1 OpenBSD 5.9-stable

    $ doas su
    # pkg_add py3-pip py3-bcrypt postgresql-server postgresql py3-psycopg2 git
    # su _postgresql
    $ initdb /var/postgresql/data
    $ exit
    # rcctl enable postgresql
    # rcctl start postgresql
    # su _postgresql
    $ createuser heimdalerp
    $ psql
    #> CREATE DATABASE heimdalerp OWNER heimdalerp;
    #> \q
    $ exit
    # exit
    $ mkdir -p $HOME/workspace/heimdalerp/src/
    $ cd $HOME/workspace/heimdalerp/src/
    $ git clone https://github.com/heimdalerp/heimdalerp
    $ cd ..
    $ pyvenv-3.4 .
    $ . bin/activate

At this point, typing python, python3 or python3.4 achieves the same.
But I like to use python3.4 and pip3.4 to emphasize the version:

    (heimdalerp) $ pip3.4 install --upgrade pip
    (heimdalerp) $ pip3.4 install -r src/heimdalerp/requirements.pip
    (heimdalerp) $ python3.4 manage.py migrate
    (heimdalerp) $ python3.4 manage.py createsuperuser
    (heimdalerp) $ python3.4 manage.py createinitialrevisions

### 1.2 Debian 8 / Ubuntu 16.04 LTS

    $ sudo su
    # apt-get install python3-pip python3-setuptools python3-bcrypt python3-venv postgresql postgresql-server-dev-all python3-psycopg2 git
    # su postgres
    $ createuser heimdalerp
    $ psql
    #> CREATE DATABASE heimdalerp OWNER heimdalerp;
    #> \q
    $ exit
    # exit
    $ mkdir -p $HOME/workspace/heimdalerp/src/
    $ cd $HOME/workspace/heimdalerp/src/
    $ git clone https://github.com/heimdalerp/heimdalerp
    $ cd ..
    $ pyvenv .
    $ . bin/activate

    (heimdalerp) $ pip3 install --upgrade pip
    (heimdalerp) $ pip3 install -r src/heimdalerp/requirements.pip
    (heimdalerp) $ python3 manage.py migrate
    (heimdalerp) $ python3 manage.py createsuperuser
    (heimdalerp) $ python3 manage.py createinitialrevisions

## 2. Deployment

When steps from point 1 are completed, you may now deploy your HeimdalERP instance.
Please, consider reading this [checklist](https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/) before running your instance in production.


### 2.1 OpenBSD 5.9-stable

    # doas su
    # pkg_add nginx
    # pip3 install uwsgi

### 2.2 Debian 8 / Ubuntu 16.04 LTS

    # sudo su
    # apt-get install nginx
    # pip3 install uwsgi
