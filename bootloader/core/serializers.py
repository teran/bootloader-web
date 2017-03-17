from core.models import Server, Location, Group

from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fqdn = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    mac = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    def create(self, validated_data):
        return Server.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fqdn = validated_data.get('fqdn', instance.fqdn)
        instance.mac = validated_data.get('mac', instance.mac)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        return instance
