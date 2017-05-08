from django.core.exceptions import ObjectDoesNotExist
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers
from servers.models import Server
from tools.models import Agent, Credential


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
        c = Credential.objects.create(
            name=validated_data['name'],
            content_object=validated_data['content_object'])
        c.encrypt(validated_data['decrypt'])
        c.save()

        return c


class AgentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    queue = serializers.CharField(
        required=True, allow_blank=False, max_length=255)
    agent_url = serializers.CharField(
        required=True, allow_blank=False, max_length=255)

    class Meta:
        model = Agent

    def create(self, validated_data):
        try:
            agent = Agent.objects.get(
                queue=validated_data['queue'])
            agent.agent_url = validated_data['agent_url']
            agent.save()
        except ObjectDoesNotExist:
            agent = Agent.objects.create(**validated_data)

        return agent
