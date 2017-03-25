from django.contrib.auth.models import User

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


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
