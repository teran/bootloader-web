from django.core.exceptions import ValidationError
from django.test import TestCase

from deployments.models import Profile


class ProfileObjectTestCase(TestCase):
    def test_profile_create(self):
        profileData = {
            'kind': 'Profile',
            'name': 'testprofile',
            'version': '0.1-blah'
        }

        profile = Profile.objects.create_profile(
            profile=profileData)

        self.assertDictEqual(profile.profile, profileData)
        self.assertEqual(profile.name, 'testprofile')
        self.assertEqual(profile.version, '0.1-blah')

    def test_profile_create_with_wrong_kind(self):
        profileData = {
            'kind': 'UnrecognizedYAML',
            'name': 'testprofile',
            'version': '0.1-blah'
        }

        with self.assertRaises(ValidationError):
            Profile.objects.create_profile(profile=profileData)

    def test_profile_create_with_absent_kind(self):
        profileData = {
            'name': 'testprofile',
            'version': '0.1-blah'
        }

        with self.assertRaises(ValidationError):
            Profile.objects.create_profile(profile=profileData)
