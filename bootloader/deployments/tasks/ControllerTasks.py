from celery import chain
from celery.utils.log import get_task_logger

from deployments.tasks import app


logger = get_task_logger(__name__)


@app.task
def echo(message):
    logger.info('Task echo: %s' % (message,))

    return True


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

    tasks = []
    steps = (
        'new',
        'preparing',
        'installing',
        'configuring',
        'postconfiguring',
        'complete',)

    workflow = d.profile.profile['workflow']

    for step in steps:
        if step in workflow and workflow[step] != {}:
            logger.info('Step %s added to queue' % (step))
            tasks.append(evaluate_step.s(deployment=d.pk, step=step))

    chain(tasks).apply_async(queue='bootloader_tasks')


@app.task
def evaluate_step(*args, **kwargs):
    logger.info('Evaluating step: %s, %s' % (args, kwargs))
    from deployments.models import Deployment, LogEntry
    from deployments.workflow import Step, WorkflowException

    d = Deployment.objects.get(pk=kwargs['deployment'])
    if d.status != 'error':
        d.evaluate(target=kwargs['step'])
        d.save()
    else:
        logger.error('WorkflowException raised on evaluate_step(%s, %s)' % (
            args, kwargs))
        raise WorkflowException(
            "Status become error. Can't continue ; d=%s" % (d.pk))

    LogEntry(
        deployment=d,
        level='INFO',
        message='Evaluating step %s for deployment pk=%s' % (
            kwargs['step'], d.pk)
    ).save()

    s = Step(
        kwargs['deployment'],
        d.profile.profile['workflow'].get(kwargs['step'], {}))
    try:
        result = s.evaluate()
    except Exception as e:
        LogEntry(
            deployment=d,
            level='CRITICAL',
            message='Error in step %s: %s' % (kwargs['step'], e)
        ).save()
        d.evaluate(target='error')
        d.save()
        logger.error(
            'WorkflowException exception raised at evaluate_step(%s, %s)' % (
                args, kwargs))
        raise

    return result
