from __future__ import unicode_literals
import hashlib
import random
import string

from django.conf import settings
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


def _generate_token():
    return hashlib.sha256(
        ''.join(random.choice(string.ascii_uppercase) for _ in range(1024))
        ).hexdigest()


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
    token = models.CharField(max_length=64, default=_generate_token)

    def __str__(self):
        return '%s@%s' % (self.profile, self.server)

    def __unicode__(self):
        return self.__str__()

    def file_export_url(self):
        return '%sexport/file/%s/%s/%s/%s/' % (
            settings.BOOTLOADER_URL,
            self.pk,
            self.token,
            self.profile.name,
            self.profile.version)
