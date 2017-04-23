from __future__ import unicode_literals
import re

from django.utils.text import slugify
from django.db import models

from tools.models import BaseModel

IPMI_BROWSER_PROTO_CHOICES = (
    (None, 'None'),
    (1, 'http'),
    (2, 'https'),
)


class Label(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class Location(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()

    def queue_name(self):
        return slugify('deployment_%s_%s' % (self.pk, self.name))


class Server(BaseModel):
    fqdn = models.CharField(max_length=255, unique=True)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='servers')
    notes = models.CharField(max_length=255, null=True)
    labels = models.ManyToManyField(Label, related_name='servers')
    serial = models.CharField(max_length=255, null=True)
    ipmi_host = models.CharField(max_length=255)
    ipmi_username = models.CharField(max_length=255, null=True)
    ipmi_password = models.CharField(max_length=255, null=True)
    ipmi_browser_proto = models.IntegerField(
        choices=IPMI_BROWSER_PROTO_CHOICES, null=True)
    ipmi_browser_port = models.IntegerField(default=80)

    def __str__(self):
        return self.fqdn

    def __unicode__(self):
        return self.__str__()

    def link_webui(self):
        return '/servers/%s/%s.html' % (self.pk, self.fqdn)

    def link_webui_edit(self):
        return '/servers/%s/%s.html?action=edit' % (self.pk, self.fqdn)

    def link_api(self):
        return '/api/servers/%s' % (self.pk)

    def link_ipmi_web(self):
        return '%s://%s' % (
            IPMI_BROWSER_PROTO_CHOICES[self.ipmi_browser_proto][1],
            self.ipmi_host)


class Interface(BaseModel):
    name = models.CharField(max_length=16)
    mac = models.CharField(max_length=17, unique=True)
    server = models.ForeignKey(Server, related_name='interfaces')

    def __str__(self):
        return '%s@%s' % (self.name, self.server.fqdn)

    def __unicode__(self):
        return self.__str__()

    def mac_dashed(self):
        return re.sub(':', '-', self.mac.lower())
