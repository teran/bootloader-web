from celery import chain
from celery.result import allow_join_result
import os

from deployments.tasks import app


STATUSES = (
    'new',
    'preparing',
    'installing',
    'configuring',
    'postconfiguring',
    'complete',
)


def DeploymentContext(deployment, custom_fields={}):
    from django.template import Context
    from deployments.models import Deployment

    d = Deployment.objects.get(pk=deployment)

    context = Context({
        'fqdn': d.server.fqdn,
        'profile': d.profile.name,
        'ipmi_host': d.server.ipmi_host,
        'export_base': d.file_export_url(),
    })

    context.update(custom_fields)

    return context


class Step():
    def __init__(self, deployment, step):
        from deployments.models import Deployment
        self.step = step
        self.deployment = Deployment.objects.get(pk=deployment)

    def evaluate(self):
        # tasks = []
        with allow_join_result():
            for s in self.step:
                print('Task %s added to queue' % (s))
                getattr(self, s['action'])(**s).get(
                    timeout=60*3,
                    propagate=True,
                    interval=1)

    def serve_file(self, *args, **kwargs):
        from django.template import Template

        from deployments.models import LogEntry

        LogEntry(
            deployment=self.deployment,
            level='DEBUG',
            message='serve_file instruction: %s ; %s' % (args, kwargs)
        ).save()

        try:
            serve_type = kwargs['source']['type']
        except KeyError as e:
            LogEntry(
                deployment=self.deployment,
                level='CRITICAL',
                message='Profile error! serve_file.source.type: %s' % (e)
            ).save()
            self.deployment.evaluate(target='error')
            self.deployment.save()
            print(
                'WorkflowException raised on step serve_file(%s, %s)' % (
                    args, kwargs))
            raise WorkflowException(
                "Profile error! serve_file.source.type ; p=%s ; d=%s" % (
                    self.deployment.profile.pk, self.deployment.pk))

        prefixes = {
            'http': '/var/lib/http',
            'tftp': '/var/lib/tftp'
        }

        if serve_type == 'url':
            try:
                source = kwargs['source']['url']
            except Exception as e:
                LogEntry(
                    deployment=self.deployment,
                    level='CRITICAL',
                    message='Profile error! serve_file.url: %s' % (e)
                ).save()
                self.deployment.evaluate(target='error')
                self.deployment.save()
                print(
                    'WorkflowException raised on step serve_file(%s, %s)' % (
                        args, kwargs))
                raise WorkflowException(
                    "Profile error! p=%s ; d=%s ; e=%s" % (
                        self.deployment.profile.pk, self.deployment.pk, e))
        elif serve_type == 'template':
            name = kwargs['source']['name']
            source = os.path.join(self.deployment.file_export_url(), name)

        filename_raw = os.path.join(
            prefixes[kwargs['via']], kwargs['filename'])

        tasks = []
        for interface in self.deployment.server.interfaces.all():
            template = Template(filename_raw)
            context = DeploymentContext(self.deployment.pk, custom_fields={
                'mac_address_dashed': interface.mac_dashed
            })
            filename = template.render(context)

            LogEntry(
                deployment=self.deployment,
                level='INFO',
                message='Sending task download_file( %s, %s )' % (
                    source, filename)
            ).save()

            tasks.append(
                app.send_task(
                    'deployments.tasks.AgentTasks.download_file',
                    kwargs={
                        'deployment': self.deployment.pk,
                        'source': source,
                        'destination': filename
                    },
                    queue=self.deployment.queue()))

        return chain(tasks)

    def delete_file(self, *args, **kwargs):
        from deployments.models import LogEntry

        filename = kwargs['filename']

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task delete_file( %s )' % (filename)
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.delete_file',
            kwargs={'deployment': self.deployment.pk, 'filename': filename},
            queue=self.deployment.queue())

    def echo(self, *args, **kwargs):
        return app.send_task(
            'deployments.tasks.AgentTasks.echo',
            kwargs={'message': kwargs['message']},
            queue=self.deployment.queue())

    def expect_callback(self, *args, **kwargs):
        print('expect_callback: %s, %s' % (args, kwargs))
        from deployments.models import LogEntry

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task expect_callback(%s)' % (kwargs['name'])
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.expect_callback',
            kwargs={
                'deployment': self.deployment.pk,
                'callback_name': kwargs['name']
            },
            queue=self.deployment.queue())

    def ipmi_command(self, *args, **kwargs):
        return app.send_task(
            'deployments.tasks.AgentTasks.ipmi_command',
            kwargs={
                'deployment': self.deployment.pk,
                'command': kwargs['command'],
                'parameters': kwargs['parameters'],
            },
            queue=self.deployment.queue())


class WorkflowException(Exception):
    pass
