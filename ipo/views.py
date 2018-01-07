# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.http import JsonResponse

def datetime_now(request):
    return JsonResponse(dict(now=datetime.datetime.now()))
