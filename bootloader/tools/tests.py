# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from deployments.models import Server
from tools.models import Credential

import random
import string


class Yaml2JsonTestCase(TestCase):
    def setUp(self):
        self.data = {'key': 'value'}
        self.yaml = b'key: value'

    def test_conversion(self):
        client = Client(enforce_csrf_checks=False)
        fileData = SimpleUploadedFile('test.yaml', self.yaml)

        result = client.post('/tools/yaml2json', {
            'yaml': fileData})

        self.assertEqual(result.json(), self.data)


class GravatarTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            'testuser', 'test@example.com', 'secret')

    def test_proxy(self):
        client = Client()
        client.login(username='testuser', password='secret')
        result = client.get('/tools/gravatar?size=80&proxy=true')

        self.assertEqual(result.status_code, 200)

    def test_redirect(self):
        client = Client()
        client.login(username='testuser', password='secret')
        result = client.get('/tools/gravatar?size=80&proxy=false')

        self.assertEqual(result.status_code, 302)

    def test_access_noauth(self):
        client = Client()
        result = client.get('/tools/gravatar?size=80&proxy=false')

        self.assertEqual(result.status_code, 302)


class CredentialTestCase(TestCase):
    def test_encryption(self):
        test_string = str(''.join(
            random.choice(
                string.ascii_uppercase) for _ in range(999)).encode('utf-8'))

        s = Server.objects.create(fqdn='test')
        c = Credential.objects.create(
            content_object=s,
            name='testcredential')
        c.encrypt(test_string)
        c.save()

        c = s.credentials.get(name='testcredential')
        decrypted_string = c.decrypt()

        self.assertEqual(test_string, decrypted_string)
