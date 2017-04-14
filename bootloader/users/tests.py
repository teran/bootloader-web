from django.test import Client, TestCase


class TestUsersAndAuthentication(TestCase):
    def setUp(self):
        self.client = Client()

        self.urls = {
            '/': 302,
            '/servers/index.html': 302,
            '/servers/locations.html': 302,
            '/deployments/deployments.html': 302,
            '/deployments/profiles.html': 302,
            '/user/events.html': 302,
            '/user/tokens.html': 302,
            '/user/profile.html': 302,
            '/user/logout.html': 302,
            '/user/login.html': 200,
            '/user/register.html': 200,
        }

    def test_unauthorized_access(self):
        results = {
            url: self.client.get(url).status_code for url in self.urls.keys()
        }

        self.assertEqual(results, self.urls)
