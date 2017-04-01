from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from deployments.models import Deployment


def file(request, deployment, token, profile, version, file):
    deployment = get_object_or_404(Deployment, pk=deployment, token=token)
    profile = deployment.profile

    contents = None
    for f in profile.profile.get('files'):
        if f.get('name') == file:
            contents = f.get('contents')

    context = Context({
        'profile': deployment.profile,
        'server': deployment.server,
    })
    template = Template(contents)

    return HttpResponse(template.render(context), content_type='text/plain')
