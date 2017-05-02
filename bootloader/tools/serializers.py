from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from servers.models import Server
from tools.models import Credential


class CredentialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    data = serializers.CharField(
        required=True, source='decrypt')
    content_object = GenericRelatedField({
        Server: serializers.HyperlinkedRelatedField(
            queryset=Server.objects.all(),
            view_name='server-detail',
        ),
    })

    class Meta:
        model = Credential

    def create(self, validated_data):
        print(validated_data)
        c = Credential.objects.create(
            name=validated_data['name'],
            content_object=validated_data['content_object'])
        c.encrypt(validated_data['decrypt'])
        c.save()

        return c
