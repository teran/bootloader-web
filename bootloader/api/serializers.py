from django.contrib.auth.models import User
from servers.models import Interface, Server, Location
from deployments.models import Profile, File, FILE_TYPES, FILE_ACCESS_TYPES
from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    fqdn = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(), slug_field='name')
    serial = serializers.CharField(required=False, allow_blank=True, max_length=255)
    ipmi_host = serializers.CharField(required=False, allow_blank=True, max_length=255)
    interfaces = serializers.SlugRelatedField(
        required=False, read_only=True, many=True, slug_field='name')

    class Meta:
        model = Server

    def create(self, validated_data):
        return Server.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fqdn = validated_data.get('fqdn', instance.fqdn)
        instance.location = validated_data.get('location', instance.location)
        instance.serial = validated_data.get('serial', instance.serial)
        instance.ipmi_host = validated_data.get(
            'ipmi_host', instance.ipmi_host)
        instance.save()

        return instance


class InterfaceSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=16)
    mac = serializers.CharField(max_length=17)
    server = serializers.SlugRelatedField(
        queryset=Server.objects.all(), slug_field='fqdn')

    class Meta:
        model = Interface

    def create(self, validated_data):
        return Interface.objects.create(**validated_data)


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    servers = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='fqdn')

    class Meta:
        model = Location
        fields = ('name',)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)


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
        if validated_data.get('profile', {}).has_key('files'):
            for file in validated_data.get('profile').get('files'):
                File.objects.create(
                    name=file.get('name'),
                    contents=file.get('contents'),
                    profile=profile).save()
        return profile


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()

    class Meta:
        model = User

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)

        instance.save()

        return instance

class FileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    filetype = serializers.ChoiceField(FILE_TYPES)
    accesstype = serializers.ChoiceField(FILE_ACCESS_TYPES)
    profile = serializers.SlugRelatedField(
        queryset=Profile.objects.all(), slug_field='pk')

    def create(self, validated_data):
        return File.objects.create(**validated_data)
