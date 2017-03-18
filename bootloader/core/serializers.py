from core.models import Server, Location, Group, IPMI_BROWSER_PROTO_CHOICES

from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fqdn = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    mac = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    serial = serializers.CharField(allow_blank=True, max_length=255)
    ipmi_host = serializers.CharField(allow_blank=True, max_length=255)
    #ipmi_browser_proto = serializers.ChoiceField(
    #    choices=IPMI_BROWSER_PROTO_CHOICES, allow_null=True)

    def create(self, validated_data):
        return Server.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fqdn = validated_data.get('fqdn', instance.fqdn)
        instance.mac = validated_data.get('mac', instance.mac)
        instance.location = validated_data.get('location', instance.location)
        instance.serial = validated_data.get('serial', instance.serial)
        ipmi_host = validated_data.get('ipmi_host', instance.ipmi_host)
        # ipmi_browser_proto = validated_data.get('ipmi_browser_proto', instance.ipmi_browser_proto)
        instance.save()

        return instance

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
