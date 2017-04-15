import json

from django.test import TestCase

from deployments.models import Profile


class ProfileObjectTestCase(TestCase):
    def setUp(self):
        self.profile = {
            'kind': 'Profile',
            'name': 'testprofile',
            'version': '0.1'
        }

    def test_profile_create(self):
        profile = Profile.objects.create(
            name='testprofile',
            version='0.1',
            profile=json.dumps(self.profile))

        self.assertDictEqual(json.loads(profile.profile), self.profile)
