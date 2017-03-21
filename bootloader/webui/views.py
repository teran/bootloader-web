from django.shortcuts import get_object_or_404, render_to_response

from core.models import Location, Server

def index(request):
    servers = Server.objects.all()

    return render_to_response(
        'webui/servers/servers.html.j2',
        context={
            'servers': servers,
            'view': 'servers'
        })


def locations(request):
    servers = Location.objects.all()

    return render_to_response(
        'webui/servers/locations.html.j2',
        context={
            'locations': locations,
            'view': 'locations'
        })


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
