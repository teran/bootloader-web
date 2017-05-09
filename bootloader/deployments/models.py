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
        unique_together = (('name', 'version', 'is_active'),)
        ordering = ['-created']

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
    progress = models.FloatField(default=0.0)

    objects = DeploymentManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '%s@%s' % (self.profile, self.server)

    def __unicode__(self):
        return self.__str__()

    def color_class_css(self):
        classes = {
            'new': '',
            'preparing': 'info',
            'installing': 'info',
            'configuring': 'info',
            'postconfiguring': 'info',
            'complete': 'success',
            'error': 'danger',
        }
        return classes[self.status]

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

    def evaluate(self, target):
        from celery.result import allow_join_result
        from deployments.workflow import Step

        getattr(self, 'set_%s' % (target,))()

        workflow = self.profile.profile['workflow']

        try:
            if target in workflow and workflow[target] != {}:
                with allow_join_result():
                    step = Step(
                        self.pk,
                        self.profile.profile['workflow'][target]
                    ).evaluate()
                    if step is not None:
                        step.wait()
        except Exception as e:
            LogEntry.objects.create(
                deployment=self,
                level='CRITICAL',
                message=e.message,
            ).save()
            self.status = 'error'
            self.save()
            raise

    @transition(
        field=status,
        source='new',
        target='preparing',
        on_error='error')
    def set_new(self):
        self.progress += 16.6
        self.status = 'preparing'
        self.save()

    @transition(
        field=status,
        source='preparing',
        target='installing',
        on_error='error')
    def set_preparing(self):
        self.progress += 16.6
        self.status = 'installing'
        self.save()

    @transition(
        field=status,
        source='installing',
        target='configuring',
        on_error='error')
    def set_installing(self):
        self.progress += 16.6
        self.status = 'configuring'
        self.save()

    @transition(
        field=status,
        source='configuring',
        target='postconfiguring',
        on_error='error')
    def set_configuring(self):
        self.progress += 16.6
        self.status = 'postconfiguring'
        self.save()

    @transition(
        field=status,
        source='postconfiguring',
        target='complete',
        on_error='error')
    def set_postconfiguring(self):
        self.progress += 16.6
        self.status = 'complete'
        self.save()

    @transition(
        field=status,
        source='complete',
        on_error='error')
    def set_complete(self):
        self.progress = 100
        self.save()

    def progress_class_css(self):
        if self.status == 'error':
            return 'progress-bar-danger'
        if self.status == 'success':
            return 'progress-bar-success'
        return 'progress-bar-info progress-bar-striped active'

    def progress_percents(self):
        return self.progres * 100

    def queue(self):
        return self.server.location.queue_name()


class LogEntry(BaseModel):
    LEVEL_CHOICES = (
        ('DEBUG', 'DEBUG',),
        ('INFO', 'INFO',),
        ('WARNING', 'WARNING',),
        ('CRITICAL', 'CRITICAL',),
    )
    deployment = models.ForeignKey(Deployment, related_name='logs')
    level = models.CharField(
        max_length=8, choices=LEVEL_CHOICES, default='INFO')
    message = models.TextField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return '%s  %s  %s' % (self.timestamp, self.level, self.message)

    def __unicode__(self):
        return self.__str__()

    def color_class_css(self):
        classes = {
            'DEBUG': '',
            'INFO': 'info',
            'WARNING': 'warning',
            'CRITICAL': 'danger',
        }

        return classes[self.level]
