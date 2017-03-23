from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from servers.models import Server


class Profile(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Deployment(models.Model):
    server = models.ForeignKey(Server, related_name='deployments')
    profile = models.ForeignKey(Profile, related_name='deployments')
    parameters = JSONField()

    def __str__(self):
        return '%s@%s' % (self.profile, self.server)

    def __unicode__(self):
        return self.__str__()
