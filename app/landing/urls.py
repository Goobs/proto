# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import *


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='landing/index.html'), name='index'),
    url(r'^subscribe/?$', SubscribeView.as_view(), name='subscribe'),
)
