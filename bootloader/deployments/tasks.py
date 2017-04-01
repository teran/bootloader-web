from django.conf import settings

from celery import Celery

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    import time
    time.sleep(30)
    print 'OK'


@app.task
def deploy_pxe_files(server):
    print 'OK'
