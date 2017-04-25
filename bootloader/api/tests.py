from __future__ import unicode_literals

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User


class APIv1alpha1TestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.org',
            password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.basic_auth_client = APIClient()
        self.basic_auth_client.login(
            username='testuser', password='testpassword')

        self.token_auth_client = APIClient()
        self.token_auth_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.handlers = [
            'deployments',
            'interfaces',
            'locations',
            'profiles',
            'servers',
            'ssh_authorized_keys',
            'users',
        ]

    def test_basic_auth(self):
        result = self.basic_auth_client.get(
            '/api/v1alpha1/', format='json').status_code

        self.assertEqual(result, 200)

    def test_token_auth(self):
        result = self.token_auth_client.get(
            '/api/v1alpha1/', format='json').status_code

        self.assertEqual(result, 200)

    def test_api_exports(self):
        result = self.token_auth_client.get(
            '/api/v1alpha1/', format='json').json()

        self.assertEqual(sorted(result.keys()), sorted(self.handlers))
