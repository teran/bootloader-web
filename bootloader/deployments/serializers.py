from deployments.models import Profile, FILE_TYPES, FILE_ACCESS_TYPES
from rest_framework import serializers


class DeploymentSerializer(serializers.Serializer):
    server = serializers.SlugRelatedField(
        required=False, read_only=True, many=True, slug_field='fqdn')
    profile = serializers.SlugRelatedField(
        required=False, read_only=True, many=True, slug_field='name')

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
        if 'files' in validated_data.get('profile', {}):
            for file in validated_data.get('profile').get('files'):
                File.objects.create(
                    name=file.get('name'),
                    contents=file.get('contents'),
                    profile=profile).save()
        return profile
