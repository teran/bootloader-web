import os

from celery import chain
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


def DeploymentContext(deployment):
    from django.template import Context
    from deployments.models import Deployment

    d = Deployment.objects.get(pk=deployment)

    context = Context({
        'fqdn': d.server.fqdn,
        'profile': d.profile.name,
        'ipmi_host': d.server.ipmi_host,
        'mac_address': d.server.interfaces.all()[0].mac,
        'mac_address_dashed': d.server.interfaces.all()[0].mac_dashed(),
        'interface_name': d.server.interfaces.all()[0].name,
        'export_base': d.file_export_url(),
    })

    return context


class Step():
    def __init__(self, deployment, step):
        self.step = step
        self.deployment = deployment

    def evaluate(self):
        from celery import signature

        tasks = []
        for s in self.step:
            logger.info('Task %s added to queue' % (s))
            tasks.append(signature(getattr(self, s['action'])(**s)))

        chain(tasks)

    def serve_file(self, *args, **kwargs):
        from django.template import Template

        from deployments.models import Deployment, LogEntry
        from deployments.tasks import app

        d = Deployment.objects.get(pk=self.deployment)

        LogEntry(
            deployment=d,
            level='DEBUG',
            message='serve_file instruction: %s ; %s' % (args, kwargs)
        ).save()

        try:
            serve_type = kwargs['source']['type']
        except KeyError as e:
            LogEntry(
                deployment=d,
                level='CRITICAL',
                message='Profile error! serve_file.source.type: %s' % (e)
            ).save()
            d.evaluate(target='error')
            d.save()
            logger.error(
                'WorkflowException raised on step serve_file(%s, %s)' % (
                    args, kwargs))
            raise WorkflowException(
                "Profile error! serve_file.source.type ; p=%s ; d=%s" % (
                    d.profile.pk, d.pk))

        prefixes = {
            'http': '/var/lib/http',
            'tftp': '/var/lib/tftp'
        }

        if serve_type == 'url':
            try:
                source = kwargs['source']['url']
            except Exception as e:
                LogEntry(
                    deployment=d,
                    level='CRITICAL',
                    message='Profile error! serve_file.url: %s' % (e)
                ).save()
                d.evaluate(target='error')
                d.save()
                logger.error(
                    'WorkflowException raised on step serve_file(%s, %s)' % (
                        args, kwargs))
                raise WorkflowException(
                    "Profile error! p=%s ; d=%s ; e=%s" % (
                        d.profile.pk, d.pk, e))
        elif serve_type == 'template':
            name = kwargs['source']['name']
            source = os.path.join(d.file_export_url(), name)

        filename_raw = os.path.join(
            prefixes[kwargs['via']], kwargs['filename'])

        template = Template(filename_raw)
        context = DeploymentContext(d.pk)
        filename = template.render(context)

        LogEntry(
            deployment=d,
            level='INFO',
            message='Sending task download_file( %s, %s )' % (source, filename)
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.download_file',
            args=(d.pk, source, filename,),
            queue=d.server.location.queue_name())

    def delete_file(self, *args, **kwargs):
        from deployments.models import Deployment, LogEntry
        from deployments.tasks import app

        d = Deployment.objects.get(pk=self.deployment)

        filename = kwargs['filename']

        LogEntry(
            deployment=d,
            level='INFO',
            message='Sending task delete_file( %s )' % (filename)
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.delete_file',
            args=(d.pk, filename),
            queue=d.server.location.queue_name())

    def echo(self, *args, **kwargs):
        from deployments.tasks import app

        return app.send_task(
            'deployments.tasks.ControllerTasks.echo',
            args=(kwargs['message'],),
            queue='bootloader_tasks')

    def expect_callback(self, *args, **kwargs):
        logger.info('expect_callback: %s, %s' % (args, kwargs))
        from deployments.models import Deployment, LogEntry
        from deployments.tasks import app

        d = Deployment.objects.get(pk=self.deployment)

        LogEntry(
            deployment=d,
            level='INFO',
            message='Sending task expect_callback(%s)' % (kwargs['name'])
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.expect_callback',
            args=(d.pk, kwargs['name']),
            queue=d.server.location.queue_name())

    def ipmi_command(self, *args, **kwargs):
        logger.info('ipmi_command: %s, %s' % (args, kwargs))


class WorkflowException(Exception):
    pass
