from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys

import psycopg2
import select
from django.db import connection as django_connection
from ipo.models import Job
from ipo.management.commands import ipo_insert_job

class Command(ipo_insert_job.Command):
    help = 'Insert and wait for Job'

    def add_arguments(self, parser):
        parser.add_argument('url')

    def handle(self, *args, **kwargs):
        job = super(Command, self).handle(*args, **kwargs)
        channel_name = 'ipo_job_done_' + str(job.id).replace('-', '')
        cursor = django_connection.cursor()
        django_connection.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor.execute('LISTEN %s' % channel_name)
        epoll = select.epoll()
        epoll.register(django_connection.connection, select.EPOLLIN)
        self.fileno_to_callback = dict()
        self.fileno_to_callback[django_connection.connection.fileno()] = self.do_data_from_database
        while True:
            self.loop(epoll)

    def loop(self, epoll):
        for fileno, event in epoll.poll():
            self.fileno_to_callback[fileno](fileno, event)

    def do_data_from_database(self, fileno, event):
        django_connection.connection.poll()
        while django_connection.connection.notifies:
            notify = django_connection.connection.notifies.pop()
            print('#%s - %s' % (notify.channel, notify.payload))

