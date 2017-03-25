from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets

from servers.models import Interface, Location, Server
from deployments.models import Profile

from api.serializers import InterfaceSerializer
from api.serializers import LocationSerializer
from api.serializers import ServerSerializer
from api.serializers import UserSerializer
from api.serializers import ProfileSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
