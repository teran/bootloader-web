from celery import group
from celery.result import allow_join_result
import os
import socket

from deployments.tasks import AgentTasks
from servers.models import Network
from tools.models import Agent


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
    import netaddr

    d = Deployment.objects.get(pk=deployment)
    ipaddress = netaddr.IPAddress(socket.gethostbyname(d.server.fqdn))
    network = Network.objects.get(network__net_contains=ipaddress)
    agent = Agent.objects.get(queue=d.queue())

    context = Context({
        'agent_url': agent.url,
        'callback_base': '%s/_callback/%s/' % (agent.agent_url, d.token,),
        'domain': '.'.join(d.server.fqdn.split('.')[1:]),
        'export_base': d.file_export_url(),
        'fqdn': d.server.fqdn,
        'gateway': network.gateway,
        'hostname': d.server.fqdn.split('.')[0],
        'ipaddress': ipaddress,
        'ipmi_host': d.server.ipmi_host,
        'nameserver': network.nameserver,
        'netmask': network.netmask,
        'profile': d.profile.name,
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
                getattr(self, s['action'])(**s).apply_async().get(
                    timeout=60*20,
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

            tasks.append(AgentTasks.download_file.signature(
                args=(),
                kwargs={
                    'deployment': self.deployment.pk,
                    'source': source,
                    'destination': filename
                }, queue=self.deployment.queue()))

        return group(tasks)

    def delete_file(self, *args, **kwargs):
        from deployments.models import LogEntry

        filename = kwargs['filename']

        LogEntry(
            deployment=self.deployment,
            level='INFO',
            message='Sending task delete_file( %s )' % (filename)
        ).save()

        return AgentTasks.delete_file.signature(
            args=(),
            kwargs={'deployment': self.deployment.pk, 'filename': filename},
            queue=self.deployment.queue())

    def echo(self, *args, **kwargs):
        return AgentTasks.echo.signature(
            args=(),
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

        return AgentTasks.expect_callback.signature(
            args=(),
            kwargs={
                'deployment': self.deployment.pk,
                'callback_name': kwargs['name']
            },
            queue=self.deployment.queue())

    def ipmi_command(self, *args, **kwargs):
        return AgentTasks.ipmi_command.signature(
            args=(),
            kwargs={
                'deployment': self.deployment.pk,
                'command': kwargs['command'],
                'parameters': kwargs['parameters'],
            },
            queue=self.deployment.queue())


class WorkflowException(Exception):
    pass
