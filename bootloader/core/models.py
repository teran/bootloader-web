from __future__ import unicode_literals

from django.db import models


IPMI_BROWSER_PROTO_CHOICES = (
    (1, 'http'),
    (2, 'https')
)


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Server(models.Model):
    fqdn = models.CharField(max_length=255, unique=True)
    mac = models.CharField(max_length=15, unique=True)
    location = models.ForeignKey(Location, related_name='servers')
    groups = models.ManyToManyField(Group, related_name='servers')
    serial = models.CharField(max_length=255, null=True)
    ipmi_host = models.CharField(max_length=255, unique=True, null=True)
    ipmi_username = models.CharField(max_length=255, null=True)
    ipmi_password = models.CharField(max_length=255, null=True)
    ipmi_browser_proto = models.IntegerField(
        choices=IPMI_BROWSER_PROTO_CHOICES, null=True)
