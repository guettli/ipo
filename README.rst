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
#. If some process is listening on the output channel, this process get notified and it can read the response from the database.


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


Retry and number of workers
===========================

At least in the beginning the ipo-server will have one process and one thread. I guess this will
be enough since the server does only async io, it does no processing.

It is up to the http servers which process the URLs to have a queue of worker processes.

The ipo-server does not do any queing. If you insert 1k URLs, then it will open 1k URLs.

If the http response is "503 Service Unavailable" the ipo-server will check the Retry-After header
of the response and will retry accordingly. See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After


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


Do later list
=============

* Writing response to DB. Write the data in several small chunks instead of big one UPDATE? See https://dba.stackexchange.com/questions/194602/chunking-data-into-a-postgresql-bytea-column/194654#194654



Why reinvent and not reuse?
===========================

In the year 2001 I played around with twisted. It swallowed exections, which means
for me that I can't use it as rock solid basic library.

In the year 2012 I used celery, but I was not happy with it. It does too much. It is too big.

Some years later I looked at python-rq, but this is based on redis. Since we already use PostgreSQL, I want to avoid an other data storage. In some usecases persistence (`ACID <https://en.wikipedia.org/wiki/ACID>`_) is
more important than performance.

In 2016 I tried to find a tool, but there seems to be no Python based solution up to now: https://softwarerecs.stackexchange.com/questions/36331/async-job-processing-based-on-postgresql

In december 2017 I had the idea to let the daemon do no work at all. It only dispatches URLs, it does not execute the job itself.
With this decopling ("Separation of concerns") the daemon looked simple enough to start coding :-)





