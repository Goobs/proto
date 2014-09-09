# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import *
from app.utils.mail import send_mail as app_send_mail
from .forms import *


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm()

    def get_success_url(self, *args, **kwargs):
        return self.request.GET.get('next', '/')

    def post(self, request):
        self.form = LoginForm(self.request.POST)

        if not self.form.is_valid():
            return self.get(request)

        username = self.form.cleaned_data.get('username')
        password = self.form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(self.get_success_url())
            else:
                self.form.errors['username'] = [u'Аккаунт неактивен']
        else:
            self.form.errors['__all__'] = [u'Неправильный логин и пароль']
        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


def password_reset_view(request, *args, **kwargs):
    template_name = 'accounts/password/password_reset_form.html'
    email_template_name = 'mail/password_reset.html'

    return password_reset(request,
                          template_name=template_name,
                          email_template_name=email_template_name,
                          password_reset_form=PasswordResetForm)


class PasswordResetDoneView(TemplateView):
    template_name = 'accounts/password/password_reset_done.html'


def password_reset_confirm_view(request, *args, **kwargs):
    template_name = 'accounts/password/password_reset_confirm.html'
    uidb64 = kwargs.get('uidb64')
    token = kwargs.get('token')
    return password_reset_confirm(request, uidb64=uidb64, token=token, template_name=template_name,
                                  set_password_form=SetPasswordForm)


class PasswordResetCompleteView(TemplateView):
    template_name = 'accounts/password/password_reset_complete.html'


class UserChangePasswordView(TemplateView):
    template_name = 'accounts/password/password_change.html'
    form = UserChangePasswordForm

    def get_context_data(self, **kwargs):
        context = super(UserChangePasswordView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request):
        self.form = UserChangePasswordForm(self.request.POST)

        if self.form.is_valid():
            if authenticate(username=self.request.user.username,
                            password=self.form.cleaned_data.get('password')):
                request.user.set_password(self.form.cleaned_data.get('new_confirm_password'))
                request.user.save()
                messages.success(request, u'Пароль успешно изменен')
                return redirect('dashboard')
            else:
                self.form.errors['password'] = [u'Неверный текущий пароль']

        return self.get(request)


class RegistrationView(TemplateView):
    template_name = 'accounts/registration.html'
    user_form = UserRegistrationForm(prefix='user')
    registered_param = '?registered=true'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['user_form'] = self.user_form
        return context

    def get_success_url(self, *args, **kwargs):

        return '/' + self.registered_param

    def post(self, request, **kwargs):
        self.user_form = UserRegistrationForm(self.request.POST, prefix='user')

        if self.user_form.is_valid():
            user = self.user_form.save(commit=False)
            try:
                app_send_mail(subject=u'Регистрация на сайте APP',
                          to=user.email,
                          template='mail/success_registration.html',
                          context={'user': user})
            except:
                pass
            log_user = authenticate(
                username=self.user_form.cleaned_data.get('email'),
                password=self.user_form.cleaned_data.get('password'))
            auth_login(request, log_user)
            return redirect(self.get_success_url())
        return self.get(request, **kwargs)
