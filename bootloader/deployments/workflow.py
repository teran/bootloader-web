import os


def deployment_context(deployment):
    from django.template import Context
    from deployments.models import Deployment

    d = Deployment.objects.get(pk=deployment)

    context = Context({
        'fqdn': d.server.fqdn,
        'profile': d.profile.name,
        'ipmi_host': d.server.ipmi_host,
        'mac_address': d.server.interfaces.all()[0].mac,
        'mac_address_dashed': d.server.interfaces.all()[0].mac_address_dashed(),
        'interface_name': d.server.interfaces.all()[0].name,
        'export_base': d.file_export_url(),
    })

    return context

class Step():
    def __init__(self, deployment, step):
        self.step = step
        self.deployment = deployment

    def evaluate(self):
        jobs = []
        for s in self.step:
            jobs.append(getattr(self, s.get('action'))(**s))

        return jobs

    def serve_file(self, *args, **kwargs):
        from deployments.models import Deployment, LogEntry
        from deployments.tasks import AgentTasks

        d = Deployment.objects.get(pk=self.deployment)

        try:
            serve_type = kwargs['source']['type']
        except Exception as e:
            LogEntry(
                deployment=d,
                level='CRITICAL',
                message='Profile error! serve_file.source: %s' % (e)
            ).save()
            raise

        prefixes = {
            'http': '/var/lib/http',
            'tftp': '/var/lib/tftp'
        }

        if serve_type == 'url':
            try:
                source = kwargs['source']['url']
                filename = os.path.join(
                    prefixes[kwargs['via']], kwargs['filename'])
            except Exception as e:
                LogEntry(
                    deployment=d,
                    level='CRITICAL',
                    message='Profile error! serve_file.url: %s' % (e)
                ).save()
                raise

            return AgentTasks.download_file.apply_async(
                args=(d.pk, source, filename,),
                queue=d.server.location.queue_name())

    def delete_file(self, *args, **kwargs):
        print(kwargs)

    def ipmi_command(self, *args, **kwargs):
        print(kwargs)