#!/usr/bin/env python

import os

from celery import Celery
from kombu import Queue

CELERY_SETTINGS = {
    'BROKER_URL': os.environ.get('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'),
    'CELERY_CREATE_MISSING_QUEUES': True,
    'CELERY_DEFAULT_QUEUE': 'default',
    'CELERY_DEFAULT_EXCHANGE': 'tasks',
    'CELERY_DEFAULT_EXCHANGE_TYPE': 'topic',
    'CELERY_DEFAULT_ROUTING_KEY': 'task.default',
    'CELERY_QUEUES': (
        Queue('default', routing_key='task.#'),
        Queue('deployment', routing_key='deployment.#'),
    ),
    'CELERY_ROUTES': {
            'tasks.deployment_start': {
                'queue': 'deployment',
                'routing_key': 'deployment_start',
            },
    }
}

app = Celery('tasks')
app.conf.update(**CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    import time
    time.sleep(30)
    print 'OK'


@app.task
def deploy_pxe_files(server):
    print 'OK'
