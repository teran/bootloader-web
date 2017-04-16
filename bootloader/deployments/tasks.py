from django.conf import settings

from celery import Celery


app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_created(*args, **kwargs):
    pass


@app.task
def evaluate_new(*args, **kwargs):
    pass


@app.task
def evaluate_preparing(*args, **kwargs):
    pass


@app.task
def evaluate_installing(*args, **kwargs):
    pass


@app.task
def evaluate_configuring(*args, **kwargs):
    pass


@app.task
def evaluate_postconfiguring(*args, **kwargs):
    pass


@app.task
def evaluate_error(*args, **kwargs):
    pass
