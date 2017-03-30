from deployments.models import Deployment, Profile
from servers.models import Server
from rest_framework import serializers


class DeploymentSerializer(serializers.Serializer):
    server = serializers.SlugRelatedField(
        queryset=Server.objects.all(), slug_field='fqdn')
    profile = serializers.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='pk')

    class Meta:
        model = Deployment

    def create(self, validated_data):
        deployment = Deployment.objects.create(**validated_data)
        return deployment

class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    version = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    profile = serializers.JSONField(binary=True)

    class Meta:
        model = Profile

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile
