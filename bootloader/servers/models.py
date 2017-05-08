from __future__ import unicode_literals
import re

from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import netaddr
from netfields.fields import CidrAddressField, InetAddressField

from tools.models import BaseModel, Credential

IPMI_BROWSER_PROTO_CHOICES = (
    ('http', 'http'),
    ('https', 'https'),
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
    ipmi_browser_proto = models.CharField(
        choices=IPMI_BROWSER_PROTO_CHOICES,
        max_length=5,
        default='http')
    ipmi_browser_port = models.IntegerField(default=80)
    credentials = GenericRelation(
        Credential,
        object_id_field='object_id',
        related_query_name='credentials')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.fqdn

    def __unicode__(self):
        return self.__str__()

    def link_webui(self):
        return '/servers/%s/%s.html' % (self.pk, self.fqdn)

    def link_webui_edit(self):
        return '/servers/%s/%s.html?action=edit' % (self.pk, self.fqdn)

    def link_api(self):
        return '/api/v1alpha1/servers/%s' % (self.pk)

    def link_ipmi_web(self):
        return '%s://%s' % (
            self.ipmi_browser_proto,
            self.ipmi_host)

    def link_ipmi_login_web(self):
        return '%s/cgi/login.cgi' % (self.link_ipmi_web(),)


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


class Network(BaseModel):
    name = models.CharField(max_length=255)
    network = CidrAddressField(unique=True)
    gateway = InetAddressField(unique=True, store_prefix_length=False)
    nameserver = InetAddressField(store_prefix_length=False)
    location = models.ForeignKey(
        Location, null=True, blank=True, related_name='networks')

    @property
    def ipaddress(self):
        ip = netaddr.IPNetwork(str(self.network))
        return str(ip.network)

    @property
    def netmask(self):
        ip = netaddr.IPNetwork(str(self.network))
        return str(ip.netmask)
