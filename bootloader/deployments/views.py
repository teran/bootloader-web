from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from deployments.models import Deployment, Profile
from servers.models import Server


@login_required
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


def profile(request, name, version):
    profile = get_object_or_404(Profile, name=name, version=version)

    return render(
        request,
        'webui/deployments/profile.html.j2',
        context={
            'view': 'deployments',
            'subview': 'profiles',
            'profile': profile,
        })


@login_required
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
