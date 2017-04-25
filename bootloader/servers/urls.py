from django.conf.urls import url

import servers.views

urlpatterns = [
    url(r'^$', servers.views.servers),
    url(r'^servers\.html$', servers.views.servers),
    url(r'^locations\.html$', servers.views.locations),
    url(
        r'^(?P<pk>[0-9]{1,11})/(?P<fqdn>[a-z0-9\.-]{1,255}).html$',
        servers.views.server),
]
