# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.forms.jsonb import JSONField
from django.db import models


class Flower(models.Model):
    id = models.UUIDField(primary_key=True)
    url = models.URLField()
    method = models.CharField(max_length=16)
    data = JSONField()
    status = models.SmallIntegerField()
    referrer = models.URLField()
    response = models.BinaryField(null=True)
