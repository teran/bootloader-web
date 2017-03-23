from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect

from rest_framework.authtoken.models import Token

from servers.models import Location, Server


def deployment_profiles(request):
    return render(
        request,
        'webui/deployments/profiles.html.j2')

@login_required
def index(request):
    servers = Server.objects.all()

    return render(
        request,
        'webui/servers/servers.html.j2',
        context={
            'servers': servers,
            'view': 'servers'
        })


@login_required
def locations(request):
    locations = Location.objects.all()

    return render(
        request,
        'webui/servers/locations.html.j2',
        context={
            'locations': locations,
            'view': 'locations'
        })


@login_required
def server(request, pk, fqdn):
    server = get_object_or_404(Server, pk=pk, fqdn=fqdn)

    if request.GET.get('action') == 'edit':
        return render_to_response(
            'webui/servers/server-edit.html.j2',
            context={
                'server': server,
                'view': 'servers',
            })
    else:
        return render(
            request,
            'webui/servers/server.html.j2',
            context={
                'server': server,
                'view': 'servers',
            })
