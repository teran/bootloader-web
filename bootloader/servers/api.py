from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets

from servers.models import Interface, Location, Server

from servers.serializers import InterfaceSerializer
from servers.serializers import LocationSerializer
from servers.serializers import ServerSerializer


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer

    def get_queryset(self):
        queryset = Interface.objects.all()

        fqdn = self.request.query_params.get('server', None)
        if fqdn is not None:
            try:
                server = Server.objects.get(fqdn=fqdn)
            except ObjectDoesNotExist:
                return []
            queryset = Interface.objects.filter(server=server.pk)

        return queryset


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self):
        queryset = Server.objects.all()

        fqdn = self.request.query_params.get('fqdn', None)
        if fqdn is not None:
            queryset = Server.objects.filter(fqdn=fqdn)

        return queryset
