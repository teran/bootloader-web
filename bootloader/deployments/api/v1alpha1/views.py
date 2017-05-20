from rest_framework import viewsets

from deployments.models import Deployment, Profile

from deployments.api.v1alpha1.serializers import ProfileSerializer
from deployments.api.v1alpha1.serializers import DeploymentSerializer
from tools.api.permissions import StaffOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    permission_classes = (StaffOrReadOnly,)

    def get_queryset(self):
        filterq = {}
        for item in self.request.query_params.keys():
            filterq[item] = self.request.query_params.get(item)

        queryset = Profile.objects.filter(**filterq)

        return queryset


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.filter(is_active=True)
    serializer_class = DeploymentSerializer
    permission_classes = (StaffOrReadOnly,)
