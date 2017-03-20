from django.conf.urls import url

from webui import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^locations\.html$', views.locations),
    url(r'^index\.html$', views.index),
    url(r'^(?P<pk>[0-9]{1,11})/(?P<fqdn>[a-z0-9\.-]{1,255}).html$', views.server)
]
