#!/usr/bin/env python

import os

from celery import Celery
import requests

import settings

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    fileBase = 'export/file/%s/%s/%s/%s' % (
        deployment, token, profile, version)

    r = requests.get('http://bootloader:8000/%s/pxelinux' % fileBase)
    print r.content


@app.task
def deploy_pxe_files(server):
    print 'OK'
