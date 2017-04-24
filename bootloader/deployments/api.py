from rest_framework import viewsets

from deployments.models import Deployment, Profile

from deployments.serializers import ProfileSerializer
from deployments.serializers import DeploymentSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        filterq = {}
        for item in self.request.query_params.keys():
            filterq[item] = self.request.query_params.get(item)

        queryset = Profile.objects.filter(**filterq)

        return queryset


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
