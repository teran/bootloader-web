from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from servers.models import Server


DEPLOYMENT_STATUSES = (
    (1, 'Unknown',),
    (2, 'Waiting for PXEBoot',),
    (3, 'Waiting for configuration request',),
    (4, 'Installation',),
    (5, 'Configuring',),
    (6, 'OS boot',),
    (7, 'Post actions',),
)

FILE_TYPES = (
    (1, 'Static',),
    (2, 'Template',),
    (3, 'Binary',),
)

FILE_ACCESS_TYPES = (
    (1, 'API',),
    (2, 'Local',),
)


class Profile(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    profile = JSONField(default={})

    class Meta:
        unique_together = (('name', 'version'),)

    def __str__(self):
        return '%s==%s' % (self.name, self.version)

    def __unicode__(self):
        return self.__str__()


class Deployment(models.Model):
    server = models.ForeignKey(Server, related_name='deployments')
    profile = models.ForeignKey(Profile, related_name='deployments')
    status = models.IntegerField(choices=DEPLOYMENT_STATUSES, default=1)
    parameters = JSONField(default={})

    def __str__(self):
        return '%s@%s' % (self.profile, self.server)

    def __unicode__(self):
        return self.__str__()
