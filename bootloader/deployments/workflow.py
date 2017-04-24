import os

from celery import chain


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
        from deployments.models import Deployment
        self.step = step
        self.deployment = Deployment.objects.get(pk=deployment)

    def evaluate(self):
        from celery import signature

        tasks = []
        for s in self.step:
            print('Task %s added to queue' % (s))
            tasks.append(signature(getattr(self, s['action'])(**s)))

        chain(tasks)

    def serve_file(self, *args, **kwargs):
        from django.template import Template

        from deployments.models import LogEntry
        from deployments.tasks import app

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

        template = Template(filename_raw)
        context = DeploymentContext(self.deployment.pk)
        filename = template.render(context)

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task download_file( %s, %s )' % (source, filename)
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.download_file',
            args=(self.deployment.pk, source, filename,),
            queue=self.deployment.server.location.queue_name())

    def delete_file(self, *args, **kwargs):
        from deployments.models import LogEntry
        from deployments.tasks import app

        filename = kwargs['filename']

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task delete_file( %s )' % (filename)
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.delete_file',
            args=(self.deployment.pk, filename),
            queue=self.deployment.server.location.queue_name())

    def echo(self, *args, **kwargs):
        from deployments.tasks import app

        return app.send_task(
            'deployments.tasks.ControllerTasks.echo',
            args=(kwargs['message'],),
            queue='bootloader_tasks')

    def expect_callback(self, *args, **kwargs):
        print('expect_callback: %s, %s' % (args, kwargs))
        from deployments.models import LogEntry
        from deployments.tasks import app

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task expect_callback(%s)' % (kwargs['name'])
        ).save()

        return app.send_task(
            'deployments.tasks.AgentTasks.expect_callback',
            args=(self.deployment.pk, kwargs['name']),
            queue=self.deployment.server.location.queue_name())

    def ipmi_command(self, *args, **kwargs):
        print('ipmi_command: %s, %s' % (args, kwargs))


class WorkflowException(Exception):
    pass
