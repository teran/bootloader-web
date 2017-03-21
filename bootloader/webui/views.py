from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render_to_response, redirect

from core.models import Location, Server


@login_required
def index(request):
    servers = Server.objects.all()

    return render_to_response(
        'webui/servers/servers.html.j2',
        context={
            'servers': servers,
            'view': 'servers'
        })


@login_required
def locations(request):
    servers = Location.objects.all()

    return render_to_response(
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
        return render_to_response(
            'webui/servers/server.html.j2',
            context={
                'server': server,
                'view': 'servers',
            })

def user_login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(
                request,
                'webui/user/login.html.j2',
                context={
                    'message': 'Authentication data is invalid',
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password'),
                })
    else:
        return render(request,
            'webui/user/login.html.j2')

def user_logout(request):
    return logout(request)
