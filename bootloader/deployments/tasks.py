from django.conf import settings

from celery import Celery

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_created(deployment):
    d = Deployment.objects.get(pk=deployment)

    d.profile.profile.get('workflow').get('new')
