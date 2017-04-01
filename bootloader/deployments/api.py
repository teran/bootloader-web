from rest_framework import viewsets

from deployments.models import Deployment, Profile

from deployments.serializers import ProfileSerializer
from deployments.serializers import DeploymentSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DeploymentViewSet(viewsets.ModelViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
