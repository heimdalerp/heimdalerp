# HeimdalERP

Heimdal is a free and opensource ERP solution based on Django REST Framework.

It is named after Heimdallr, a god of Norse mythology.
Heimdallr is attested as possessing foreknowledge, keen eyesight and hearing, and is described as "the whitest of the gods".
He guards Bifrost, the bridge which connects the human world with Asgard, the gods' world.
It is said that he brings the gift of the gods to mankind.

## 1. Install

### 1.1 OpenBSD

a) First install its dependencies:

    # pkg_add py3-pip py3-bcrypt postgresql-server postgresql py3-psycopg2 git

b) Fetch the code. Pay attention to its branches:

    $ git clone https://github.com/mbaragiola/heimdalerp

This fetches master, which is the latest version for development.

c) Install further dependencies with pip3.4:

    # pip3.4 install -r heimdalerp/requirements.pip

d) Setup the database.

    # su _postgresql
    $ initdb /var/postgresql/data
    $ exit
    # rcctl enable postgresql
    # rcctl start postgresql

If you want a clean start (i.e first time using HeimdalERP), do as follows:

    # su _postgresql
    $ createuser -s heimdalerp
    $ psql
    #> CREATE DATABASE heimdalerp OWNER heimdalerp;
    #> \q

e) Initialize your applications data:

    $ python3.4 manage.py migrate
    $ python3.4 manage.py createinitialrevisions

