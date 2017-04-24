from django.contrib.auth.models import User

from rest_framework import viewsets

from users.models import SSHAuthorizedKey
from users.serializers import UserSerializer, SSHAuthorizedKeySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SSHAuthorizedKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHAuthorizedKey.objects.all()
    serializer_class = SSHAuthorizedKeySerializer
