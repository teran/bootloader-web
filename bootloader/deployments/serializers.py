from deployments.models import Deployment, Profile
from deployments import tasks

from servers.models import Server
from rest_framework import serializers

from slugify import slugify


class DeploymentSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    server = serializers.SlugRelatedField(
        queryset=Server.objects.all(), slug_field='fqdn')
    profile = serializers.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='pk')
    token = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = Deployment

    def create(self, validated_data):
        deployment = Deployment.objects.create(**validated_data)

        tasks.deployment_start.apply_async(
            args=[deployment.pk],
            queue=slugify(
                'deployment_%s_%s' % (
                    deployment.server.location.pk,
                    deployment.server.location.name),
                to_lower=True))

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
