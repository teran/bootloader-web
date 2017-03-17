from __future__ import unicode_literals

from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Server(models.Model):
    fqdn = models.CharField(max_length=255, unique=True)
    mac = models.CharField(max_length=15, unique=True)
    location = models.ForeignKey(Location, related_name='servers')
    groups = models.ManyToManyField(Group, related_name='servers')
