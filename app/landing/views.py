# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from robokassa.forms import RobokassaForm
from .forms import *
from .models import *


class IndexView(TemplateView):
    form = None

    def get_template_names(self):
        return ['landing/index.html']

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if not self.form:
            self.form = SubscribeForm()
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        self.form = SubscribeForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            messages.success(request, u'Cпасибо за регистрацию')
            payment = Payment.objects.create(
                user=self.form.instance,
                sum=100,
                description=u'Оплата семинара'
            )
            request.session['payment'] = payment.pk
            request.session.save()
            return redirect('subscribe')

        return self.get(request, **kwargs)


class SubscribeView(TemplateView):
    template_name = 'landing/subscribe.html'
    form = None

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        payment_id = self.request.session.get('payment')
        payment = get_object_or_404(Payment, pk=payment_id)
        if not self.form:
            self.form = RobokassaForm(initial={
                'OutSum': payment.sum,
                'InvId': payment.pk,
                'Desc': payment.description,
                'Culture': 'ru'
            })
        context['form'] = self.form
        return context
