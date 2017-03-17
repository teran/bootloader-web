from django.shortcuts import render_to_response

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
