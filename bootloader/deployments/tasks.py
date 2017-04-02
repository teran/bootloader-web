from django.conf import settings

from celery import Celery

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    pass


@app.task
def download_file(URL, target):
    pass
