# HeimdalERP

Heimdal is a free and opensource ERP solution based on Django REST Framework.

It is named after Heimdallr, a god of Norse mythology.
Heimdallr is attested as possessing foreknowledge, keen eyesight and hearing, and is described as "the whitest of the gods".
He guards Bifrost, the bridge which connects the human world with Asgard, the gods' world.
It is said that he brings the gift of the gods to mankind.

## 1. Install from source

### 1.1 OpenBSD 6.0-stable

    $ doas su
    # pkg_add py3-pip postgresql-server postgresql py3-psycopg2 git
    # su _postgresql
    $ initdb /var/postgresql/data
    $ exit
    # rcctl enable postgresql
    # rcctl start postgresql
    # su _postgresql
    $ createuser --createdb heimdalerp
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

    (heimdalerp) $ pip3 install --upgrade pip
    (heimdalerp) $ pip3 install -r src/heimdalerp/requirements/common.pip
    (heimdalerp) $ python3 manage.py migrate
    (heimdalerp) $ python3 manage.py createsuperuser
    (heimdalerp) $ python3 manage.py createinitialrevisions

### 1.2 Debian 8 / Ubuntu 16.04 LTS

    $ sudo su
    # apt-get install libffi-dev python3-pip python3-setuptools python3-venv postgresql postgresql-server-dev-all python3-psycopg2 git
    # su postgres
    $ createuser --createdb heimdalerp
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
    (heimdalerp) $ pip3 install -r src/heimdalerp/requirements/common.pip
    (heimdalerp) $ python3 manage.py migrate
    (heimdalerp) $ python3 manage.py createsuperuser
    (heimdalerp) $ python3 manage.py createinitialrevisions

## 2. Deployment

When steps from point 1 are completed, you may now deploy your HeimdalERP instance.
Please, consider reading this [checklist](https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/) before running your instance in production.

If you have your files at $HOME/workspace/heimdalerp, you need to copy them,symlink them, clone them again from git or configure your user/group and your OS webserver's user/group to access it.

In our case, we'll clone it again at /var/www/heimdalerp and recreate the virtualenv. In this way, we have a two separate enviroments, one for development and testing, and the other for production use. Be aware, that in this case they are using the very same database. You may set separate databases creating another one and modifying heimdalerp/settings.py to use it (search for const var "DATABASE").

### 2.1 OpenBSD 6.0-stable

    # doas su
    # pkg_add nginx
    # pip3 install uwsgi

### 2.2 Debian 8 / Ubuntu 16.04 LTS

    # sudo su
    # apt-get install nginx
    # pip3 install uwsgi
    # mkdir -p /var/www/heimdalerp/src/
    # cd /var/www/heimdalerp/src/
    # git clone https://github.com/heimdalerp/heimdalerp
    # cd ..
    # . bin/activate
    (heimdalerp) # pip3 install --upgrade pip
    (heimdalerp) # pip3 install -r src/heimdalerp/requirements/common.pip

Now you need to create a folder named static and point it in heimdalerp/settings.py (search for const vars named "STATIC").    

    (heimdalerp) # cd src/heimdalerp && mkdir djangostatic
    (heimdalerp) # vi heimdalerp/settings.py
    (heimdalerp) # python3 manage.py collectstatic
    (heimdalerp) # deactivate
    # cp /etc/nginx/uwsgi_params .
    # ln -s common/deployment/heimdalerp_nginx.conf /etc/nginx/sites-enabled/ 
    # chown -R www-data:www-data /var/www/heimdalerp
    # service nginx restart
    # mkdir -p /etc/uwsgi/vassals
    # ln -s common/deployment/heimdalerp_uwsgi.ini /etc/uwsgi/vassals/

Add to /etc/rc.local:

    /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
