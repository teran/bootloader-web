"""bootloader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

import servers.views

urlpatterns = [
    url(r'^$', servers.views.servers),
    url(r'^api/', include('api.v1alpha2.urls')),
    url(r'^api/v1alpha1/', include('api.v1alpha1.urls')),
    url(r'^api/v1alpha2/', include('api.v1alpha2.urls')),
    url(r'^deployments/', include('deployments.urls')),
    url(r'^export/', include('export.urls')),
    url(r'^servers/', include('servers.urls')),
    url(r'^tools/', include('tools.urls')),
    url(r'^user/', include('users.urls')),
]
