from django.conf.urls import url

import deployments.views

urlpatterns = [
    url(r'^deployments\.html$', deployments.views.deployments),
    url(r'^profiles\.html$', deployments.views.profiles),
]
