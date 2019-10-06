# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'register/$', views.apiregister, name='apiregister'),
    url(r'^report/?$', views.report, name='report'),
    url(r'login/$', views.apilogin, name='apilogin'),
    url(r'verify/$', views.verify, name='verify'),
    url(r'settodo/([0-9]+)/$', views.settodo, name='settodo'),
    url(r'student/([0-9]+)/$', views.student, name='student'),
    url(r'loogout/$', views.logout, name='logout'),

    # The home page
    url(r'^$', views.index, name='index'),
]

