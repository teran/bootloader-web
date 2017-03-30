from django.conf.urls import url, include

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'deployments', views.DeploymentViewSet)
router.register(r'interfaces', views.InterfaceViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'servers', views.ServerViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
