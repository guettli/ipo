from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import psycopg2
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Run IPO server (endless loop)'
    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        connection.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        assert 0
