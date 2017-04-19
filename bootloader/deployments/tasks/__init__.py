from celery import Celery

from django.conf import settings

app = Celery('deployment')
app.conf.update(**settings.CELERY_SETTINGS)
