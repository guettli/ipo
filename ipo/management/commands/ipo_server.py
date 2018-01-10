from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import select
import sys
import traceback

import psycopg2
import requests
from django.core.management.base import BaseCommand
from django.db import connection as django_connection
from ipo.models import Job
from thread import start_new_thread

insert_channel_name = 'ipo_job_insert'


class Command(BaseCommand):
    help = 'Run IPO server (endless loop)'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def loop(self, epoll):
        for fileno, event in epoll.poll():
            self.fileno_to_callback[fileno](fileno, event)

    def handle(self, *args, **kwargs):
        cursor = django_connection.cursor()
        django_connection.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor.execute('LISTEN %s' % insert_channel_name)
        epoll = select.epoll()
        epoll.register(django_connection.connection, select.EPOLLIN)
        sys.stdout.write('listening on %s\n' % insert_channel_name)
        self.fileno_to_callback = dict()
        self.fileno_to_callback[django_connection.connection.fileno()] = self.do_data_from_database
        while True:
            self.loop(epoll)

    def do_data_from_database(self, fileno, event):
        django_connection.connection.poll()
        while django_connection.connection.notifies:
            notify = django_connection.connection.notifies.pop()
            print('#%s - %s' % (notify.channel, notify.payload))
            job = Job.objects.get(id=notify.payload)
            start_new_thread(self.fetch_url_in_thread, (job,))

    def fetch_url_in_thread(self, job):
        method = getattr(requests, job.method)
        try:
            response = method(job.url)
        except Exception as exc:
            job.traceback = traceback.format_exc()
            job.status = Job.STATUS_FAILED
            job.save()
            return
        job.status = response.status_code
        job.response_content = response.content
        job.response_header = response.headers
        job.save()
