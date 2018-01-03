Input Processing Output
=======================

https://en.wikipedia.org/wiki/IPO_model

IPO is an open source asynchronous job queue which is based on PostgreSQL.

In this implementation a job is an URL.

Status
======

Brainstorming, not usable up to now.

Steps
=====

#. The IPO daemon gets started. It uses the PostgreSQL LISTEN method to wait for changes in the database.
#. You insert a new URL into the database table ipo_job.
#. The IPO daemon will get a notification via PostgreSQL NOTIFY on the input channel.
#. The IPO daemon opens the URL and puts the open file descriptor into its event loop.
#. If the URL response gets received, the IPO daemon will store the response and executes a NOTIFY on the output channel.
#. If some process is listening on the output channel, this process get notified and it can read the resopnse from the database.


How to insert a new job into the queue?
=======================================

You insert a new job into the queue by adding a new row into the database table ipo_job.

You need to supply these values:

* url: The URL which does the actual processing.
* method: The http method. Usually "get" or "post"
* data (optional): If your method is "post"


How to receive the notification as soon as the response arrives?
===============================================================

LISTEN on the particular output channel. The name of the output channel contains the UUID of the job-URL: "ipo_job_response_{UUID}".


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


Why reinvent and not reuse?
===========================

In the year 2001 I played around with twisted. It swallowed exections, which means
for me that I can't use it as rock solid basic library.

In the year 2012 I used celery, but I was not happy with it. It does too much. It is too big.

Some years later I looked at python-rq, but this is based on redis. Up to now we don't use redis
and I need a persistent queue which survives server reboots. In some usecases persistence is
more important than performance.

In 2016 I tried to find a tool, but there seems to be no Python based solution up to now: https://softwarerecs.stackexchange.com/questions/36331/async-job-processing-based-on-postgresql

In december 2017 I had the idea to let the daemon do no work at all. It only dispatches URLs, it does not execute the job itself.
With this decopling ("Separation of concerns") the daemon looked simple enough to start coding :-)





