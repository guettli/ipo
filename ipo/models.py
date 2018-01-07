# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.postgres.forms.jsonb import JSONField
from django.db import models


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    method = models.CharField(max_length=16, default='get')
    data = JSONField()
    status = models.SmallIntegerField(default=0)
    referrer = models.URLField()
    response_header = JSONField()
    response_content = models.BinaryField(null=True)
    traceback = models.TextField(default='')

    STATUS_WAITING = 0
    STATUS_RUNNING = 1
    STATUS_FAILED = 2
    STATUS_OK = 200

    def __unicode__(self):
        return 'Job %s' % self.id
