Input Processing Output
=======================

https://en.wikipedia.org/wiki/IPO_model

IPO is an open source asynchronous job queue which is based on PostgreSQL.

Design Goals
============

* Simple
* Don't think twice before creating conditions (if-statements). Think three times!
* Avoid nullable columns in your schema.

Create Database
===============

Replace "guettli" with the name of your linux user account.

    postgres@pc> createuser guettli
    postgres@pc> createdb -O guettli ipo-env


Create Virtualenv
=================

    guettli@pc> virtualenv ipo-env
    guettli@pc> cd ipo-env
    guettli@pc> . .bin/activate.sh
    guettli@pc> pip install -e git+https://github.com/guettli/ipo.git#egg=ipo
    guettli@pc> python src/ipo/ipo_site/manage.py migrate


