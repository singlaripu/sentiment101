# sentiment/webapp/urls.py

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^search', views.search, name='search')
)