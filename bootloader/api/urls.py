from django.conf.urls import url, include

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'servers', views.ServerViewSet)
router.register(r'locations', views.LocationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
