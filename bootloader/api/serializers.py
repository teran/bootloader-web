from core.models import Interface, Server, Location, Group, IPMI_BROWSER_PROTO_CHOICES

from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fqdn = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    location = serializers.SlugRelatedField(queryset=Location.objects.all(), slug_field='name')
    serial = serializers.CharField(allow_blank=True, max_length=255)
    ipmi_host = serializers.CharField(allow_blank=True, max_length=255)
    interfaces = serializers.SlugRelatedField(read_only=True, many=True, slug_field='name')

    class Meta:
        model = Server

    def create(self, validated_data):
        return Server.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fqdn = validated_data.get('fqdn', instance.fqdn)
        instance.location = validated_data.get('location', instance.location)
        instance.serial = validated_data.get('serial', instance.serial)
        ipmi_host = validated_data.get('ipmi_host', instance.ipmi_host)
        # ipmi_browser_proto = validated_data.get('ipmi_browser_proto', instance.ipmi_browser_proto)
        instance.save()

        return instance

class InterfaceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=16)
    server = serializers.SlugRelatedField(queryset=Server.objects.all(), slug_field='fqdn')

    class Meta:
        model = Interface

    def create(self, validated_data):
        return Interface.objects.create(**validated_data)

class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    servers = serializers.SlugRelatedField(read_only=True, many=True, slug_field='fqdn')

    class Meta:
        model = Location
        fields = ('name',)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)
