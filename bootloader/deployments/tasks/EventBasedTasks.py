from deployments.tasks import app


@app.task
def deployment_created(deployment):
    from deployments.models import Deployment, LogEntry
    from deployments.tasks import ControllerTasks

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='INFO',
        message='Deployment pk=%s created for %s with %s' % (
            d.pk, d.server, d.profile)
    ).save()

    result = ControllerTasks.evaluate_deployment.apply_async(
        args=(d.pk,), queue='bootloader_tasks')
    print(result)
