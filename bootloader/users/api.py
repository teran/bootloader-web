from django.contrib.auth.models import User

from rest_framework import viewsets

from tools.api.permissions import OwnerOrReadOnly, StaffOrReadOnly
from users.models import SSHAuthorizedKey
from users.serializers import UserSerializer, SSHAuthorizedKeySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (StaffOrReadOnly,)


class SSHAuthorizedKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHAuthorizedKey.objects.filter(is_active=True)
    serializer_class = SSHAuthorizedKeySerializer
    permission_classes = (OwnerOrReadOnly,)
