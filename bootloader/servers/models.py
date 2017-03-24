from __future__ import unicode_literals
import re

from django.db import models


IPMI_BROWSER_PROTO_CHOICES = (
    (None, 'None'),
    (1, 'http'),
    (2, 'https'),
)


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Server(models.Model):
    fqdn = models.CharField(max_length=255, unique=True)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='servers')
    groups = models.ManyToManyField(Group, related_name='servers')
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


class Interface(models.Model):
    name = models.CharField(max_length=16)
    mac = models.CharField(max_length=15, unique=True)
    server = models.ForeignKey(Server, related_name='interfaces')

    def __str__(self):
        return '%s@%s' % (self.name, self.server.fqdn)

    def __unicode__(self):
        return self.__str__()

    def mac_address_dashed(self):
        return re.sub(':', '-', self.mac.lower())
