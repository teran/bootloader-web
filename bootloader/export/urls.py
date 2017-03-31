from django.conf.urls import url

from export import views

urlpatterns = [
    url(r'^file\/(?P<deployment>[0-9]+)\/(?P<token>[a-f0-9]{64})\/(?P<profile>[a-zA-Z0-9\._-]+)\/(?P<version>[0-9\.]+)\/(?P<file>[a-zA-Z0-9\._-]+)$', views.file),
]
