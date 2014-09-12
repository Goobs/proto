# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class PaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Payment, PaymentAdmin)
