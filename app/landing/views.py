# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from .forms import *


class SubscribeView(TemplateView):
    template_name = 'landing/index.html'
