from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from tools.models import Credential
from tools.serializers import CredentialSerializer


class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        filterq = {}
        for item in self.request.query_params.keys():
            filterq[item] = self.request.query_params.get(item)

        queryset = Credential.objects.filter(**filterq)

        return queryset
