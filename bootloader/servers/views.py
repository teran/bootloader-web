from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from servers.models import Location, Server


@login_required
def servers(request):
    filter_options = {
        'fqdn': 'fqdn__contains',
        'ipmi_host': 'ipmi_host',
        'location': 'location__name__contains',
        'serial': 'serial',
    }
    filterq = {}
    try:
        for param in request.GET.keys():
            filterq[filter_options[param]] = request.GET.get(param)

        servers = Server.objects.filter(**filterq)
    except KeyError:
        servers = []

    locations = Location.objects.all()

    return render(
        request,
        'webui/servers/servers.html.j2',
        context={
            'locations': locations,
            'servers': servers,
            'view': 'servers',
            'subview': 'servers',
        })


@login_required
def locations(request):
    locations = Location.objects.all()

    return render(
        request,
        'webui/servers/locations.html.j2',
        context={
            'locations': locations,
            'view': 'servers',
            'subview': 'locations'
        })


@login_required
def server(request, pk, fqdn):
    server = get_object_or_404(Server, pk=pk, fqdn=fqdn)

    if request.GET.get('action') == 'edit':
        return render(
            request,
            'webui/servers/server-edit.html.j2',
            context={
                'server': server,
                'view': 'servers',
                'subview': 'servers',
            })
    else:
        return render(
            request,
            'webui/servers/server.html.j2',
            context={
                'server': server,
                'view': 'servers',
                'subview': 'servers',
            })
