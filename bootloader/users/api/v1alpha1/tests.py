from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework.test import APIClient


class TestAuthentication(TestCase):
    def setUp(self):
        self.urls_noauth = {
            '/': 302,
            '/api/': 401,
            '/api/v1alpha1/': 401,
            '/deployments/deployments.html': 302,
            '/deployments/profiles.html': 302,
            '/servers/index.html': 404,
            '/servers/locations.html': 302,
            '/servers/servers.html': 302,
            '/tools/yaml2json': 200,
            '/user/events.html': 302,
            '/user/login.html': 200,
            '/user/logout.html': 302,
            '/user/profile.html': 302,
            '/user/register.html': 200,
            '/user/sshkeys.html': 302,
            '/user/tokens.html': 302,
        }

        self.urls_auth_nostaff = {
            '/': 200,
            '/api/': 200,
            '/api/v1alpha1/': 200,
            '/deployments/deployments.html': 200,
            '/deployments/profiles.html': 200,
            '/servers/index.html': 404,
            '/servers/locations.html': 200,
            '/servers/servers.html': 200,
            '/tools/yaml2json': 200,
            '/user/events.html': 302,
            '/user/login.html': 200,
            '/user/logout.html': 302,
            '/user/profile.html': 200,
            '/user/register.html': 200,
            '/user/sshkeys.html': 200,
            '/user/tokens.html': 200,
        }

        self.urls_authstaff = {
            '/': 200,
            '/api/': 200,
            '/api/v1alpha1/': 200,
            '/deployments/deployments.html': 200,
            '/deployments/profiles.html': 200,
            '/servers/index.html': 404,
            '/servers/locations.html': 200,
            '/servers/servers.html': 200,
            '/tools/yaml2json': 200,
            '/user/events.html': 200,
            '/user/login.html': 200,
            '/user/logout.html': 302,
            '/user/profile.html': 200,
            '/user/register.html': 200,
            '/user/sshkeys.html': 200,
            '/user/tokens.html': 200,
        }

        User.objects.create_user('testuser', 'testuser@example.org', 'secret')
        u = User.objects.create_user(
            'teststaffuser', 'testuser@example.org', 'secret')
        u.is_staff = True
        u.save()

    def test_unauthorized_access(self):
        results = {}
        for url in self.urls_noauth.keys():
            client = Client()
            results[url] = client.get(url).status_code

        self.assertEqual(results, self.urls_noauth)

    def test_authorized_access(self):
        results = {}
        for url in self.urls_auth_nostaff.keys():
            client = Client()
            client.login(username='testuser', password='secret')
            results[url] = client.get(url).status_code

        self.assertEqual(results, self.urls_auth_nostaff)

    def test_authorized_access_with_staff_perm(self):
        results = {}
        for url in self.urls_authstaff.keys():
            client = Client()
            client.login(username='teststaffuser', password='secret')
            results[url] = client.get(url).status_code

        self.assertEqual(results, self.urls_authstaff)


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

    def test_user_activation(self):
        testuser = User.objects.create_user(
            'testuser', 'testuser@example.org', 'secret')
        testuser.is_active = False
        testuser.save()

        staffuser = User.objects.create_user(
            'staffuser', 'testuser@example.org', 'secret')
        staffuser.is_active = True
        staffuser.is_staff = True
        staffuser.save()

        client = APIClient()
        client.login(username='staffuser', password='secret')
        result = client.patch(
            '/api/v1alpha1/users/%s/' % (testuser.pk,),
            data={
                'is_active': True
            },
            format='json')

        self.assertEqual(result.status_code, 200)

    def test_user_staff(self):
        testuser = User.objects.create_user(
            'testuser', 'testuser@example.org', 'secret')
        testuser.is_active = False
        testuser.save()

        staffuser = User.objects.create_user(
            'staffuser', 'testuser@example.org', 'secret')
        staffuser.is_active = True
        staffuser.is_staff = True
        staffuser.save()

        client = APIClient()
        client.login(username='staffuser', password='secret')
        result = client.patch(
            '/api/v1alpha1/users/%s/' % (testuser.pk,),
            data={
                'is_staff': True
            },
            format='json')

        self.assertEqual(result.status_code, 200)
