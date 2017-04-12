from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from deployments.models import Deployment


def file(request, deployment, token, profile, version, file):
    deployment = get_object_or_404(
        Deployment,
        pk=deployment,
        token=token,
        profile__name=profile,
        profile__version=version)
    profile = deployment.profile

    try:
        contents = profile.profile.get('files').get(file).get('contents')
    except KeyError:
        raise Http404

    context = Context({
        'profile': deployment.profile,
        'server': deployment.server,
        'export_base': deployment.file_export_url,
    })
    template = Template(contents)

    return HttpResponse(template.render(context), content_type='text/plain')
