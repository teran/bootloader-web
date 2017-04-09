from django.conf.urls import url

from tools import views

urlpatterns = [
    url(r'^yaml2json$', views.yaml2json),
]
