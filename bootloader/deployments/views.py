
from django.shortcuts import render

from deployments.models import Deployment, Profile


def deployments(request):
    deployments = Deployment.objects.all()

    return render(
        request,
        'webui/deployments/deployments.html.j2',
        context={
            'view': 'deployments',
            'subview': 'deployments',
            'deployments': deployments,
        })


def profiles(request):
    profiles = Profile.objects.all()

    return render(
        request,
        'webui/deployments/profiles.html.j2',
        context={
            'view': 'deployments',
            'subview': 'profiles',
            'profiles': profiles,
        })
