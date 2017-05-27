from __future__ import unicode_literals

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User


class APIv1alpha2TestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.org',
            password='testpassword')
        self.user.is_staff = True
        self.user.save()
        self.token = Token.objects.create(user=self.user)

        self.noauth_client = APIClient()

        self.basic_auth_client = APIClient()
        self.basic_auth_client.login(
            username='testuser', password='testpassword')

        self.token_auth_client = APIClient()
        self.token_auth_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.handlers = [
            'agents',
            'credentials',
            'deployments',
            'interfaces',
            'labels',
            'locations',
            'networks',
            'profiles',
            'servers',
            'ssh_authorized_keys',
            'users',
        ]

        self.api_versions = [
            'v1alpha2',
        ]

        self.urls_noauth = {}
        self.urls_auth = {}

        for version in self.api_versions:
            for handler in self.handlers:
                if version not in self.urls_noauth:
                    self.urls_noauth[version] = {}
                if version not in self.urls_auth:
                    self.urls_auth[version] = {}
                self.urls_auth[version][handler] = 200
                self.urls_noauth[version][handler] = 401

    def test_noauth(self):
        result = {}
        for version in self.api_versions:
            for handler in self.handlers:
                if version not in result:
                    result[version] = {}
                result[version][handler] = self.noauth_client.get(
                    '/api/%s/%s/' % (version, handler,),
                    format='json').status_code

        self.assertEqual(result, self.urls_noauth)

    def test_basic_auth(self):
        result = {}
        for version in self.api_versions:
            for handler in self.handlers:
                if version not in result:
                    result[version] = {}
                result[version][handler] = self.basic_auth_client.get(
                    '/api/%s/%s/' % (version, handler,),
                    format='json').status_code

        self.assertEqual(result, self.urls_auth)

    def test_token_auth(self):
        result = {}
        for version in self.api_versions:
            for handler in self.handlers:
                if version not in result:
                    result[version] = {}
                result[version][handler] = self.token_auth_client.get(
                    '/api/%s/%s/' % (version, handler,),
                    format='json').status_code

        self.assertEqual(result, self.urls_auth)

    def test_api_exports(self):
        result = self.token_auth_client.get(
            '/api/v1alpha2/', format='json').json()

        self.assertEqual(sorted(result.keys()), sorted(self.handlers))
