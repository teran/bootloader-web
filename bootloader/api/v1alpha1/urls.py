from django.conf.urls import url, include

from rest_framework import routers

import deployments.api
import servers.api
import users.api

router = routers.DefaultRouter()
router.register(r'deployments', deployments.api.DeploymentViewSet)
router.register(r'interfaces', servers.api.InterfaceViewSet)
router.register(r'locations', servers.api.LocationViewSet)
router.register(r'profiles', deployments.api.ProfileViewSet)
router.register(r'servers', servers.api.ServerViewSet)
router.register(r'ssh_authorized_keys', users.api.SSHAuthorizedKeyViewSet),
router.register(r'users', users.api.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
