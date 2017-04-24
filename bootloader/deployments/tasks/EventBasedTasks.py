from deployments.tasks import app


@app.task
def deployment_created(deployment):
    from deployments.models import Deployment, LogEntry
    from deployments.workflow import STATUSES

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='INFO',
        message='Deployment pk=%s created for %s with %s' % (
            d.pk, d.server, d.profile)
    ).save()

    for step in STATUSES:
        d.evaluate(target=step)
