from django.contrib.auth.models import User
from django.db import models

from tools.models import BaseModel


class SSHAuthorizedKey(BaseModel):
    key = models.TextField
    user = models.ForeignKey(User, related_name='ssh_authorized_keys')

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.__str__()
