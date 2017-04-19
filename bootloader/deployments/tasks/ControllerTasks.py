from deployments.tasks import app


@app.task
def evaluate_deployment(deployment):
    from deployments.models import Deployment, LogEntry

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='INFO',
        message='Evaluating deployment pk=%s for %s with %s' % (
            d.pk, d.server, d.profile)
    ).save()

    evaluate_step.apply_async(
        args=(d.pk, 'new',), queue='bootloader_tasks') | \
        evaluate_step.apply_async(
            args=(d.pk, 'preparing',), queue='bootloader_tasks') | \
        evaluate_step.apply_async(
            args=(d.pk, 'installing',), queue='bootloader_tasks') | \
        evaluate_step.apply_async(
            args=(d.pk, 'configuring',), queue='bootloader_tasks') | \
        evaluate_step.apply_async(
            args=(d.pk, 'postconfiguring',),     queue='bootloader_tasks')


@app.task
def evaluate_step(deployment, step):
    from deployments.models import Deployment, LogEntry
    from deployments.workflow import Step

    d = Deployment.objects.get(pk=deployment)

    LogEntry(
        deployment=d,
        level='INFO',
        message='Evaluating step %s for deployment pk=%s' % (step, d.pk)
    ).save()

    s = Step(deployment, d.profile.profile['workflow'][step])
    try:
        for job in s.evaluate():
            print(job)
    except Exception as e:
        LogEntry(
            deployment=d,
            level='CRITICAL',
            message='Error in step %s: %s' % (step, e)
        ).save()
        d.evaluate(target='error')
        d.save()
