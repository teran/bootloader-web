from django.conf.urls import url

import deployments.views

urlpatterns = [
    url(r'^deployments\.html$', deployments.views.deployments),
    url(
        r'^profiles/(?P<name>[a-z0-9_-]+)/(?P<version>[0-9\.]+).html',
        deployments.views.profile),
    url(r'^profiles\.html$', deployments.views.profiles),
]
