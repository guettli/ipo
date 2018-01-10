from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import select

import psycopg2
import sys
from django.core.management.base import BaseCommand
from django.db import connection as django_connection
from ipo.models import Job


class Command(BaseCommand):
    help = 'Insert Job'

    def add_arguments(self, parser):
        parser.add_argument('url')

    def handle(self, *args, **kwargs):
        url=kwargs.pop('url')
        job = Job.objects.create(url=url)
        sys.stdout.write('%s\n' % job)
        return job
