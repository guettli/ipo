from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import select

import psycopg2
from django.core.management.base import BaseCommand
from django.db import connection as django_connection


class Command(BaseCommand):
    help = 'Run IPO server (endless loop)'

    @classmethod
    def handle_event(cls, fileno, event):
        assert 0, (fileno, event)

    @classmethod
    def loop(cls, epoll):
        for fileno, event in epoll.poll():
            cls.handle_event(fileno, event)

    def handle(self, *args, **kwargs):
        cursor = django_connection.cursor()
        django_connection.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cursor.execute('LISTEN ipo_job--insert')
        epoll = select.epoll()
        epoll.register(django_connection.connection, select.EPOLLIN | select.EPOLLET)
        while True:
            self.loop(epoll)
