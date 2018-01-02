# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os

import re
import subx

import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipo_site.settings")
import django
django.setup()
import subprocess
import tempfile
from django.db import connection as django_connection
from django.db import connections

import os

import signal
from django.test import TestCase
from ipo.models import Job


class IPOServerTestCase(TestCase):
    longMessage = True

    def start_ipo_server(self):
        temp_file=tempfile.mktemp(prefix=self.id())
        pipe=subprocess.Popen('django-admin ipo_server > %s 2>&1' % temp_file,
                              shell=True, preexec_fn=os.setsid)
        for i in range(30):
            if os.path.exists(temp_file) and 'listening on' in open(temp_file).read():
                break
            time.sleep(0.3)
        else:
            raise AssertionError('Timeout reached. See %s' % temp_file)
        return pipe, temp_file

    def test_ipo_server_via_subprocess_pipe(self):
        pipe, temp_file = self.start_ipo_server()
        result = subx.call(['django-admin', 'ipo_insert_job', 'asdf'])
        parts = result.stdout.split()
        self.assertEqual('Job', parts[0], parts)
        job_id = parts[1]
        self.assertTrue(Job.objects.filter(id=job_id).exists(), parts)
        os.killpg(os.getpgid(pipe.pid), signal.SIGTERM)
        ret = pipe.wait()
        server_output = open(temp_file).read()
        self.assertEqual(-signal.SIGTERM, ret, server_output)
        self.assertTrue(re.match(r'^listening on ipo_job_insert\n#ipo_job_insert - \S+$',
                                 server_output), server_output)

