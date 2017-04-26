from rest_framework import viewsets

from servers.models import Interface, Location, Server

from servers.serializers import InterfaceSerializer
from servers.serializers import LocationSerializer
from servers.serializers import ServerSerializer

from tools.api.permissions import StaffOrReadOnly


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    permission_classes = (StaffOrReadOnly,)

    def get_queryset(self):
        filterq = {}
        for item in self.request.query_params.keys():
            filterq[item] = self.request.query_params.get(item)

        queryset = Server.objects.filter(**filterq)

        return queryset


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (StaffOrReadOnly,)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (StaffOrReadOnly,)

    def get_queryset(self):
        queryset = Server.objects.all()

        fqdn = self.request.query_params.get('fqdn', None)
        if fqdn is not None:
            queryset = Server.objects.filter(fqdn=fqdn)

        return queryset
