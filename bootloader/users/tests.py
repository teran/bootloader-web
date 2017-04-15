from django.contrib.auth.models import User
from django.test import Client, TestCase


class TestAuthentication(TestCase):
    def setUp(self):
        self.urls = {
            '/': 302,
            '/api/': 404,
            '/api/v1alpha1/': 401,
            '/deployments/deployments.html': 302,
            '/deployments/profiles.html': 302,
            '/servers/index.html': 302,
            '/servers/locations.html': 302,
            '/tools/yaml2json': 200,
            '/user/events.html': 302,
            '/user/login.html': 200,
            '/user/logout.html': 302,
            '/user/profile.html': 302,
            '/user/register.html': 200,
            '/user/tokens.html': 302,
        }

    def test_unauthorized_access(self):
        client = Client()
        results = {
            url: client.get(url).status_code for url in self.urls.keys()
        }

        self.assertEqual(results, self.urls)


class TestUserActions(TestCase):
    def test_user_registration(self):
        client = Client(enforce_csrf_checks=False)
        client.post('/user/register.html', {
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'testuser@example.org',
            'username': 'testuser',
            'password': 'secret',
            'password2': 'secret'})

        u = User.objects.get(username='testuser')

        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.email, 'testuser@example.org')
        self.assertEqual(u.first_name, 'Test')
        self.assertEqual(u.last_name, 'User')

    def test_user_login(self):
        User.objects.create_user('testuser', 'testuser@example.org', 'secret')
        client = Client(enforce_csrf_checks=False)
        result = client.post('/user/login.html?next=/user/profile.html', {
            'username': 'testuser',
            'password': 'secret'})

        self.assertRedirects(
            result,
            '/user/profile.html',
            status_code=302,
            target_status_code=200)
