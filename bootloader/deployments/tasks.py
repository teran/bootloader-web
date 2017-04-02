from django.conf import settings

from celery import Celery

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    pass


@app.task
def deploy_pxe_files(server):
    pass
