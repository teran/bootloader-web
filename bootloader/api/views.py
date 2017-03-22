from django.contrib.auth.models import User

from rest_framework import viewsets

from core.models import Interface, Location, Server
from api.serializers import InterfaceSerializer
from api.serializers import LocationSerializer
from api.serializers import ServerSerializer
from api.serializers import UserSerializer


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
