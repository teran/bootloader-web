from django.shortcuts import render

from deployments.models import Deployment, Profile
from servers.models import Server

def deployments(request):
    deployments = Deployment.objects.all()
    servers = Server.objects.all()
    profiles = Profile.objects.all()

    return render(
        request,
        'webui/deployments/deployments.html.j2',
        context={
            'view': 'deployments',
            'subview': 'deployments',
            'deployments': deployments,
            'servers': servers,
            'profiles': profiles,
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
