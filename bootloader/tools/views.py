# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import yaml
import json

from django.http import HttpResponse


def yaml2json(request):
    try:
        data = yaml.load(request.FILES.get('profile'))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'error', 'reason': str(e)}))
    return HttpResponse(json.dumps(data), content_type='application/json')
