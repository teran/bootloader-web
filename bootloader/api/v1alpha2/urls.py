from django.conf.urls import url, include

from rest_framework import routers

import deployments.api.v1alpha2.views
import servers.api.v1alpha2.views
import tools.api
import users.api.v1alpha2.views

router = routers.DefaultRouter()
router.register(r'agents', tools.api.AgentViewSet)
router.register(r'credentials', tools.api.CredentialViewSet)
router.register(
    r'deployments', deployments.api.v1alpha2.views.DeploymentViewSet)
router.register(r'interfaces', servers.api.v1alpha2.views.InterfaceViewSet)
router.register(r'labels', servers.api.v1alpha2.views.LabelViewSet)
router.register(r'locations', servers.api.v1alpha2.views.LocationViewSet)
router.register(r'networks', servers.api.v1alpha2.views.NetworkViewSet)
router.register(r'profiles', deployments.api.v1alpha2.views.ProfileViewSet)
router.register(r'servers', servers.api.v1alpha2.views.ServerViewSet)
router.register(
    r'ssh_authorized_keys', users.api.v1alpha2.views.SSHAuthorizedKeyViewSet),
router.register(r'users', users.api.v1alpha2.views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
