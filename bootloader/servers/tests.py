from django.db import IntegrityError
from django.test import TestCase

from servers.models import Interface, Location, Server


class InterfaceTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='TestLocation')
        self.location.save()

        self.server = Server.objects.create(
            fqdn='myserver.local', location=self.location)
        self.server.save()

    def test_interface_consistency(self):
        interface = Interface.objects.create(
            name='eth0', mac='11:11:11:11:11', server=self.server)
        interface.save()

        self.assertEqual(interface.name, 'eth0')
        self.assertEqual(interface.mac, '11:11:11:11:11')

    def test_interface_mac_uniqueness(self):
        interface = Interface.objects.create(
            name='eth0', mac='11:11:11:11:11', server=self.server)
        interface.save()

        with self.assertRaises(IntegrityError):
            Interface.objects.create(
                name='eth0', mac='11:11:11:11:11', server=self.server)


class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(name='Location1')
        Location.objects.create(name='Location2')

    def test_location_create(self):
        l = Location.objects.create(name='Location3')

        self.assertEqual(l.name, 'Location3')

    def test_location_consistency(self):
        location1 = Location.objects.get(name='Location1')
        location2 = Location.objects.get(name='Location2')

        self.assertEqual(location1.name, 'Location1')
        self.assertEqual(location2.name, 'Location2')


class ServerTestCase(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name='TestLocation')

    def test_server_create(self):
        s = Server.objects.create(fqdn='myserver.local')
        s.location = self.location
        s.save()

        self.assertEqual(s.fqdn, 'myserver.local')
        self.assertEqual(s.location, self.location)


    def test_server_fqdn_uniqueness(self):
        s1 = Server.objects.create(fqdn='myserver.local')
        s1.save()

        with self.assertRaises(IntegrityError):
            Server.objects.create(fqdn='myserver.local').save()
