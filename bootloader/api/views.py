from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from core.models import Server
from core.serializers import ServerSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
