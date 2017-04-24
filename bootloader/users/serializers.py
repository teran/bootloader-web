from django.contrib.auth.models import User

from rest_framework import serializers

from users.models import SSHAuthorizedKey


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


class SSHAuthorizedKeySerializer(serializers.Serializer):
    key = serializers.CharField()

    class Meta:
        model = SSHAuthorizedKey

    def create(self, validated_data):
        return SSHAuthorizedKey.objects.create(**validated_data)
