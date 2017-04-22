from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, Template

from deployments.models import Deployment


def file(request, deployment, token, profile, version, file):
    from deployments.workflow import deployment_context

    deployment = get_object_or_404(
        Deployment,
        pk=deployment,
        token=token,
        profile__name=profile,
        profile__version=version)
    profile = deployment.profile

    try:
        contents = profile.profile['templates'][file]['contents']
    except KeyError:
        raise Http404

    context = deployment_context(deployment.pk)
    template = Template(contents)

    return HttpResponse(template.render(context), content_type='text/plain')
