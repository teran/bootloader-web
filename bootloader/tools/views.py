# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import json
import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import yaml

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from tools.helpers import string2bool


def yaml2json(request):
    try:
        data = yaml.load(request.FILES.get('yaml'))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'error', 'reason': str(e)}))
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def gravatar(request):
    proxy = string2bool(request.GET.get('proxy', settings.GRAVATAR_PROXY))

    options = {
        'size': request.GET.get('size', '250'),
    }

    gravatar_url = 'https://www.gravatar.com/avatar/%s?%s' % (
        hashlib.md5(request.user.email.lower().encode('utf-8')).hexdigest(),
        urlencode(options))

    if proxy:
        r = requests.get(gravatar_url)
        return HttpResponse(
            r.content,
            content_type=r.headers.get('Content-Type', 'image/jpeg'))
    else:
        return redirect(gravatar_url)
