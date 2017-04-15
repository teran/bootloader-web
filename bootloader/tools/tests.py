# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase


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
