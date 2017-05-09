from deployments.tasks import app
from tools.notifications import Notification


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

    Notification(
        message='<%s|Deployment#%s> for <%s|%s> with <%s|%s> created' % (
            d.full_url(),
            d.pk,
            d.server.full_url(),
            d.server,
            d.profile.full_url(),
            d.profile,))

    for step in STATUSES:
        d.evaluate(target=step)


@app.task
def deployment_completed(deployment):
    from deployments.models import Deployment, LogEntry

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='INFO',
        message='Deployment pk=%s completed for %s with %s' % (
            d.pk, d.server, d.profile)
    ).save()

    Notification(
        message='<%s|Deployment#%s> for <%s|%s> with <%s|%s> created' % (
            d.full_url(),
            d.pk,
            d.server.full_url(),
            d.server,
            d.profile.full_url(),
            d.profile,))


@app.task
def deployment_failed(deployment, reason=None):
    from deployments.models import Deployment, LogEntry

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='CRITICAL',
        message='Deployment pk=%s failed for %s with %s: %s' % (
            d.pk, d.server, d.profile, reason,)
    ).save()

    Notification(
        message='<%s|Deployment#%s> for <%s|%s> with <%s|%s> created' % (
            d.full_url(),
            d.pk,
            d.server.full_url(),
            d.server,
            d.profile.full_url(),
            d.profile,
            reason,))
