from django.core.exceptions import ValidationError
from django.db import models


class ProfileManager(models.Manager):
    def create_profile(self, *args, **kwargs):
        if 'kind' not in kwargs.get('profile'):
            raise ValidationError("Provided data doesn't contain kind field")

        kind = kwargs.get('profile').get('kind')
        if kind.lower() != 'profile':
            raise ValidationError(
                "Expected kind is 'Profile', %s is passed" % kind)

        return self.create(
            name=kwargs.get('profile').get('name'),
            version=kwargs.get('profile').get('version'),
            profile=kwargs.get('profile'))
