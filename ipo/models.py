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
    response = models.BinaryField(null=True)

    def __unicode__(self):
        return 'Job %s' % self.id