from __future__ import unicode_literals
import hashlib
import json
import random
import string
import yaml

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from django_fsm import FSMField, transition

from deployments.managers import DeploymentManager, ProfileManager
from servers.models import Server
from tools.models import BaseModel

def _generate_token():
    return hashlib.sha256(
        ''.join(
            random.choice(
                string.ascii_uppercase) for _ in range(1024)).encode('utf-8')
        ).hexdigest()


class Profile(BaseModel):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    profile = JSONField(default={})

    objects = ProfileManager()

    class Meta:
        unique_together = (('name', 'version'),)

    def __str__(self):
        return '%s==%s' % (self.name, self.version)

    def __unicode__(self):
        return self.__str__()

    def json(self):
        return json.dumps(self.profile, indent=4)

    def link_webui(self):
        return '/deployments/profiles/%s/%s.html' % (
            self.name,
            self.version)

    def yaml(self):
        return yaml.safe_dump(
            self.profile,
            encoding='utf-8',
            default_flow_style=False,
            default_style=False,
            explicit_start=True,
            explicit_end=True,
            tags=False)


class Deployment(BaseModel):
    server = models.ForeignKey(Server, related_name='deployments')
    profile = models.ForeignKey(Profile, related_name='deployments')
    status = FSMField(default='new')
    parameters = JSONField(default={})
    token = models.CharField(max_length=64, default=_generate_token)

    objects = DeploymentManager()

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

    def link_webui(self):
        return '/deployments/%s/%s/%s.html' % (
            self.pk,
            self.server.fqdn,
            self.profile.name)

    @transition(field=status, source='*', target='error')
    def set_error_state(self):
        pass

    @transition(field=status, source='new', target='preparing')
    def set_preparing_state(self):
        pass
