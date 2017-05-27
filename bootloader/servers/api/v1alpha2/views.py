from rest_framework import viewsets

from servers.models import Interface, Network, Label, Location, Server

from servers.api.v1alpha2.serializers import InterfaceSerializer
from servers.api.v1alpha2.serializers import LabelSerializer
from servers.api.v1alpha2.serializers import LocationSerializer
from servers.api.v1alpha2.serializers import NetworkSerializer
from servers.api.v1alpha2.serializers import ServerSerializer

from tools.api.permissions import StaffOrReadOnly


class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.filter(is_active=True)
    serializer_class = InterfaceSerializer
    permission_classes = (StaffOrReadOnly,)

    def get_queryset(self):
        filterq = {}
        for item in self.request.query_params.keys():
            filterq[item] = self.request.query_params.get(item)

        queryset = Interface.objects.filter(**filterq)

        return queryset


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.filter(is_active=True)
    serializer_class = NetworkSerializer
    permission_classes = (StaffOrReadOnly,)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.filter(is_active=True)
    serializer_class = LabelSerializer
    permission_classes = (StaffOrReadOnly,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = (StaffOrReadOnly,)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (StaffOrReadOnly,)

    def get_queryset(self):
        queryset = Server.objects.all()

        fqdn = self.request.query_params.get('fqdn', None)
        if fqdn is not None:
            queryset = Server.objects.filter(fqdn=fqdn)

        return queryset
