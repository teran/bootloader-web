from django.contrib.contenttypes.models import ContentType
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
        if 'object' in self.request.query_params.keys():
            filterq['content_type'] = ContentType.objects.get(
                model=self.request.query_params['object']).pk

        if 'object_id' in self.request.query_params.keys():
            filterq['object_id'] = self.request.query_params['object_id']

        if 'name' in self.request.query_params.keys():
            filterq['name'] = self.request.query_params['name']

        queryset = Credential.objects.filter(**filterq)

        return queryset
