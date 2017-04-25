from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Template

from deployments.models import Deployment
from deployments.workflow import DeploymentContext


def file(request, deployment, token, profile, version, file):
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

    context = DeploymentContext(deployment.pk)
    template = Template(contents)

    return HttpResponse(template.render(context), content_type='text/plain')


def ssh_authorized_keys(request, deployment, token, profile, version, user):
    get_object_or_404(
        Deployment,
        pk=deployment,
        token=token,
        profile__name=profile,
        profile__version=version)

    u = get_object_or_404(User, username=user)

    return HttpResponse(
        "\n".join([x.key for x in u.ssh_authorized_keys.all()]),
        content_type='text/plain'
    )
