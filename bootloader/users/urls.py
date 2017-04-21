from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^events\.html$', views.user_events),
    url(r'^login\.html$', views.user_login),
    url(r'^logout\.html$', views.user_logout),
    url(r'^profile\.html$', views.user_profile),
    url(r'^register\.html$', views.user_register),
    url(r'^sshkeys\.html$', views.user_ssh_authorized_keys),
    url(r'^tokens\.html$', views.user_tokens),
]
