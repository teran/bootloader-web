from django.contrib.auth.models import User

from rest_framework import viewsets

from tools.api.permissions import OwnerOrReadOnly, StaffOrReadOnly
from users.models import SSHAuthorizedKey
from users.api.v1alpha1.serializers import UserSerializer
from users.api.v1alpha1.serializers import SSHAuthorizedKeySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (StaffOrReadOnly,)


class SSHAuthorizedKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHAuthorizedKey.objects.filter(is_active=True)
    serializer_class = SSHAuthorizedKeySerializer
    permission_classes = (OwnerOrReadOnly,)
