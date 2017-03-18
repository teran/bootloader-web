from django.shortcuts import get_object_or_404, render_to_response

from core.models import Server

def index(request):
    servers = Server.objects.all()

    return render_to_response(
        'webui/servers/index.html.j2',
        context={
            'servers': servers,
            'view': 'servers'
        })


def locations(request):
    servers = Server.objects.all()

    return render_to_response(
        'webui/servers/index.html.j2',
        context={
            'servers': servers,
            'view': 'locations'
        })


def server(request, pk, fqdn):
    server = get_object_or_404(Server, pk=pk, fqdn=fqdn)

    return render_to_response(
        'webui/servers/server.html.j2',
        context={
            'server': server,
            'view': 'servers',
        })
