Input Processing Output
=======================

https://en.wikipedia.org/wiki/IPO_model

IPO is an open source asynchronous job queue which is based on PostgreSQL.

Steps
=====

#. The IPO daemon gets started. It uses the PostgreSQL LISTEN method to wait for changes in the database.
#. You insert a new URL into the database table ipo_flower.
#. The IPO daemon will get a notification via PostgreSQL NOTIFY on the input channel.
#. The IPO daemon opens the URL and puts the open file descriptor into its event loop.
#. If the URL response gets received, the IPO daemon will store the response and NOTIFY on the output channel.
#. If some process is listening on the output channel for the output channel, this process get notified and it can read the resopnse from the database


How to insert a new job into the queue?
=======================================

You insert a new job into the queue by adding a new row into the database table ipo_flower.

You need to supply these values:

* url: The URL which does the actual processing.
* method: The http method. Usually "get" or "post"
* data (optional): If you method is "post"


How to receive the notification as soon as the response arrives?
===============================================================

LISTEN on the output channel. TODO Details!


Design Goals
============

* Simple
* Don't think twice before creating conditions (if-statements). Think three times!
* Avoid nullable columns in your schema.
* No locks. There is one "big" Linux epoll.

Create Database
===============

Replace "guettli" with the name of your linux user account.

.. code:: shell

    postgres@pc> createuser guettli
    postgres@pc> createdb -O guettli ipo-env


Create Virtualenv
=================

.. code:: python

    guettli@pc> virtualenv ipo-env
    guettli@pc> cd ipo-env
    guettli@pc> . .bin/activate.sh
    guettli@pc> pip install -e git+https://github.com/guettli/ipo.git#egg=ipo
    guettli@pc> python src/ipo/ipo_site/manage.py migrate


