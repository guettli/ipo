# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import json
import os
import re
import time

import subx

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipo_site.settings")
import django

django.setup()
import subprocess
import tempfile

import os

import signal
from django.test import TestCase
from ipo.models import Job


class IPOServerTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.start_ipo_server()
        self.web_server_pipe, self.web_server_output_path = self.start_web_server()

    def tearDown(self):
        os.killpg(os.getpgid(self.ipo_server_pipe.pid), signal.SIGTERM)
        os.killpg(os.getpgid(self.web_server_pipe.pid), signal.SIGTERM)
        ret = self.ipo_server_pipe.wait()
        ret = self.web_server_pipe.wait()

    def start_ipo_server(self):
        self.ipo_server_output_path = tempfile.mktemp(prefix=self.id())
        self.ipo_server_pipe = subprocess.Popen('django-admin ipo_server > %s 2>&1' %
                                                self.ipo_server_output_path,
                                shell=True, preexec_fn=os.setsid)
        for i in range(30):
            if os.path.exists(self.ipo_server_output_path) \
                    and 'listening on' in open(self.ipo_server_output_path).read():
                break
            if not self.ipo_server_pipe.poll() is None:
                break
            time.sleep(0.1)
        else:
            os.killpg(os.getpgid(self.ipo_server_pipe.pid), signal.SIGTERM)
            raise AssertionError('Timeout reached. See %s' % self.ipo_server_output_path)

    @property
    def http_and_host(self):
        return 'http://' + self.web_server_host_and_port

    web_server_host_and_port = 'localhost:8123'

    def start_web_server(self):
        temp_file = tempfile.mktemp(prefix=self.id())
        pipe = subprocess.Popen('django-admin runserver --noreload %s > %s 2>&1'
                                % (self.web_server_host_and_port, temp_file),
                                shell=True, preexec_fn=os.setsid)
        for i in range(30):
            if os.path.exists(temp_file) and 'Starting development server at ' in open(temp_file).read():
                break
            time.sleep(0.3)
        else:
            raise AssertionError('Timeout reached. See %s' % temp_file)
        return pipe, temp_file

    def test_invalid_url(self):
        job = self.ipo_server_via_subprocess_pipe(url='asdf')
        self.assertEqual(Job.STATUS_FAILED, job.status)
        self.assertIn("Invalid URL 'asdf'", job.traceback)

    def test_datetime_now_url(self):
        job = self.ipo_server_via_subprocess_pipe(
            url=self.http_and_host + '/ipo/datetime-now')
        self.assertEqual(Job.STATUS_OK, job.status, self.debugging_output_for_job(job))
        self.assertEqual(['now'], json.loads(str(job.response_content)).keys())

    def debugging_output_for_job(self, job):
        return '''Job {id}
{url}

{method}

{data}

{status}

{referrer}

{response}

{traceback}

----------
{ipo_server_output}
----------
{web_server_output}
       '''.format(
            id=job.id,
            url=job.url,
            method=job.method,
            data=repr(job.data),
            status=job.status,
            referrer=job.referrer,
            response=repr(job.response_content[:20]),
            traceback=job.traceback,
            web_server_output=open(self.web_server_output_path).read(),
            ipo_server_output=open(self.ipo_server_output_path).read(),
        )

    def ipo_server_via_subprocess_pipe(self, url):
        result = subx.call(['django-admin', 'ipo_insert_job', url])
        parts = result.stdout.split()
        self.assertEqual('Job', parts[0], parts)
        job_id = parts[1]
        self.assertTrue(Job.objects.filter(id=job_id).exists(), parts)
        server_output = open(self.ipo_server_output_path).read()
        match = re.match(r'^listening on ipo_job_insert\n#ipo_job_insert - (\S+)$',
                         server_output)
        self.assertTrue(match, server_output)
        job_id_again = match.group(1)
        self.assertEqual(job_id, job_id_again)
        return Job.objects.get(id=job_id)
